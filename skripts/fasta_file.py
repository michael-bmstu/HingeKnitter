import re
import os
from os import path
from tqdm import tqdm


def to_raw(string):
    return fr'{string}'


def is_exists_dir(dir):
    return os.path.exists(dir)


def file_ext(path_f):
    _, ext = os.path.splitext(path_f)
    return ext


def make_dir(dir):
    if not is_exists_dir(dir):
        print('Creating directory ' + dir)
        os.makedirs(dir)


def dir_walker(task_dir, ans_dir, hinge_file_path, prefix, min_len, pattern, task_file=None):
    make_dir(ans_dir + "\cash")
    cash_dir = ans_dir + "\cash"
    if task_file:
        for i in tqdm(range(1)):
            ans_path_long = path.join(ans_dir, prefix + "_long" + str(i + 1) + ".fasta")
            ans_path_short = path.join(ans_dir, prefix + "_short" + str(i + 1) + ".fasta")
    
            cash_path = path.join(cash_dir, prefix + "_cash" + str(i + 1) + ".fasta")
    
            data_file = FastaFile(task_file, min_len)
            res_file = ResFastaFile(hinge_file_path, data_file)

            res_file.correct_lines(pattern)
            res_file.write_data(ans_path_long, ans_path_short, cash_path)
        
    else:
        files = [
            f for f in os.listdir(task_dir)
            if file_ext(os.path.join(task_dir, f)) == ".fasta"
        ]

        for i in tqdm(range(len(files))):
    
            task_file_path = path.join(task_dir, files[i])
    
            ans_path_long = path.join(ans_dir, prefix + "_long" + str(i + 1) + ".fasta")
            ans_path_short = path.join(ans_dir, prefix + "_short" + str(i + 1) + ".fasta")
    
            cash_path = path.join(cash_dir, prefix + "_cash" + str(i + 1) + ".fasta")
    
            data_file = FastaFile(task_file_path, min_len)
            res_file = ResFastaFile(hinge_file_path, data_file)
    
            res_file.correct_lines(pattern)
            res_file.write_data(ans_path_long, ans_path_short, cash_path)


class FastaFile:
    def __init__(self, data_file_path, min_len):
        """
        :param data_file_path:
            >1 dima12_10 tufas Ab cDNA library
            LAAQLAMAQVQLVQSGGGSVRAGGSLRLSCVASGEYST
            >2 dima12_10 tufas Ab cDNA library
            ...
        """
        self.reads_short = []
        self.reads_long = []  # LAAQLAMAQVQLVQSGGGSVRAGGSLRLSCVASGEYST, ...
        self.names_short = []
        self.names_long = []  # >1 dima12_10 tufas Ab cDNA library, >2 dima12_10 tufas Ab cDNA library

        with open(data_file_path, 'r') as f:
            lines = f.readlines()
            names = [line.rstrip('\n') for line in lines[::2]]
            reads = [line.rstrip('\n') for line in lines[1::2]]

            if len(reads) != len(names):
                names.pop(-1)
            assert len(reads) == len(names)

            for i in range(len(reads)):
                if len(reads[i]) > min_len:
                    self.reads_long.append(reads[i])
                    self.names_long.append(names[i])
                else:
                    self.reads_short.append(reads[i])
                    self.names_short.append(names[i])



class ResFastaFile:
    def __init__(self, hinge_file_path, fasta_file):
        """
        :param hinge_file_path:
            >1
            GTNGGCKCPKCP
            >2
            GTNEVCKCPKCP
            >3
            AHHPEDPSSQCPKCP
            >4
            AHHSEDPSSKCPKCP
            >5
            EPKIPQPQPKPQPQPQPQPKPQPKPEPECTCPKCP
        :param fasta_file:
            class Fasta_file
        """
        self.hinge = []
        self.new_names = []
        self.new_names_short = []

        self.lines = []
        self.lines_short = []
        self.cash_lines = []  # cash
        self.cash_names = []
        self.data = fasta_file
        with open(hinge_file_path, 'r') as f:
            self.hinge = [line.rstrip('\n') for line in f.readlines()[1::2]]


    def correct_lines(self, pattern):

        """
        pattern_1 = r'(.*QVTVSS)'  # ideal
        pattern_2 = r'(.*QVTV)'  # VSS, VSA, VSV // + SS/SA/SV
        pattern_3 = r'(.*TQVT)'  # VSS, VSA, VSV, SPS, SS, SL
        pattern_er_1 = r'(.*[QRE][VI]TVSS)'  # errors read
        pattern_er_2 = r'(.*[QRE][VI]TV)'
        pattern_er_3 = r'(.*[TI][QRE][VI]T)'


        def names_lines_1(name, line):
            _lines = [0] * 3
            _lines[0] = line + "SS"
            _lines[1] = line + "SA"
            _lines[2] = line + "SV"

            _names = [0] * 3
            _names[0] = name + " SS"
            _names[1] = name + " SA"
            _names[2] = name + " SV"
            return _names, _lines

        def names_lines_2(name, line):
            _lines = [0] * 6
            _lines[0] = line + "VSS"
            _lines[1] = line + "VSA"
            _lines[2] = line + "VSV"
            _lines[3] = line + "SPS"
            _lines[4] = line + "SS"
            _lines[5] = line + "SL"

            _names = [0] * 6
            _names[0] = name + " VSS"
            _names[1] = name + " VSA"
            _names[2] = name + " VSV"
            _names[3] = name + " SPS"
            _names[4] = name + " SS"
            _names[5] = name + " SL"
            return _names, _lines
        """

        def add_hinge(name, line):
            """
            :param line: seq like ...QVTVSS
            :param name: name of line
            hinge:
                seq1, seq2, ...
            names:
                [name + 1, name + 2, ...]; list: [seq + se1, seq + seq2, ...]
            """
            names = [name + " " + str(k) for k in range(1, len(self.hinge) + 1)]
            lines = [line + h for h in self.hinge]

            return names, lines

        """
        for i in range(len(reads)):
            read = reads[i]
            if re.search(pattern_1, read):  # QVTVSS
                line = re.search(pattern_1, read).group(0)
                add_hinge(names[i], line)

            elif re.search(pattern_2, read):  # QVTV
                line = re.search(pattern_2, read).group(0)
                _names, _lines = names_lines_1(names[i], line)
                for j in range(3):
                    add_hinge(_names[j], _lines[j])

            elif re.search(pattern_3, read):  # QVT
                line = re.search(pattern_3, read).group(0)
                _names, _lines = names_lines_2(names[i], line)
                for j in range(6):
                    add_hinge(_names[j], _lines[j])

            elif re.search(pattern_er_1, read):  # QVTVSS with errors
                line = re.search(pattern_er_1, read).group(0)
                add_hinge(names[i], line)

                corr_line = line[:-6] + "QVTVSS"
                add_hinge(names[i] + " corrected", corr_line)

            elif re.search(pattern_er_2, read):  # QVTV with errors
                line = re.search(pattern_er_2, read).group(0)
                _names, _lines = names_lines_1(names[i], line)
                for j in range(3):
                    add_hinge(_names[j], _lines[j])

                corr_line = line[:-4] + "QVTV"
                _names, _lines = names_lines_1(names[i], corr_line)
                for j in range(3):
                    add_hinge(_names[j] + " corrected", _lines[j])

            elif re.search(pattern_er_3, read):  # QVT with errors
                line = re.search(pattern_er_3, read).group(0)
                _names, _lines = names_lines_2(names[i], line)
                for j in range(6):
                    add_hinge(_names[j], _lines[j])

                corr_line = line[:-4] + "TQVT"
                _names, _lines = names_lines_2(names[i], corr_line)
                for j in range(6):
                    add_hinge(_names[j] + " corrected", _lines[j])
            else:  # nothing found
                self.cash_lines.append(read)
                self.cash_names.append(names[i])
        """

        # pattern = to_raw(pattern)
        reads_long = self.data.reads_long
        names_long = self.data.names_long
        reads_short = self.data.reads_short
        names_short = self.data.names_short

        for i in range(len(reads_short)):
            read_s = reads_short[i]
            if re.search(pattern, read_s):  # pattern
                line = re.search(pattern, read_s).group(0)
                names_s, lines_s = add_hinge(names_short[i], line)
                self.new_names_short.append(names_s)
                self.lines_short.append(lines_s)

            else:  # nothing found
                self.cash_lines.append(read_s)
                self.cash_names.append(names_short[i])

        for i in range(len(reads_long)):
            read_l = reads_long[i]
            if re.search(pattern, read_l):  # pattern
                line = re.search(pattern, read_l).group(0)
                names_l, lines_l = add_hinge(names_long[i], line)
                self.new_names.append(names_l)
                self.lines.append(lines_l)

            else:  # nothing found
                self.cash_lines.append(read_l)
                self.cash_names.append(names_long[i])

    def write_data(self, long_path, short_path, cash_path):
        with open(long_path, "w") as res_f_long:
            with open(short_path, "w") as res_f_short:
                assert len(self.new_names) == len(self.lines)

                for i in range(len(self.lines)):
                    assert len(self.new_names[i]) == len(self.lines[i])

                    for j in range(len(self.lines[i])):
                        res_f_long.write(self.new_names[i][j] + '\n')
                        res_f_long.write(self.lines[i][j] + '\n')

                for i in range(len(self.lines_short)):
                    assert len(self.new_names_short[i]) == len(self.lines_short[i])

                    for j in range(len(self.lines_short[i])):
                        res_f_short.write(self.new_names_short[i][j] + '\n')
                        res_f_short.write(self.lines_short[i][j] + '\n')

        with open(cash_path, "w") as cash_f:
            assert len(self.cash_lines) == len(self.cash_names)
            for i in range(len(self.cash_lines)):
                cash_f.write(self.cash_names[i] + '\n')
                cash_f.write(self.cash_lines[i] + '\n')




