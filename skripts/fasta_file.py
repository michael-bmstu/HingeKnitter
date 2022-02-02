import re
import os
from os import path
from tqdm import tqdm


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
    """

    :param task_dir: directory with task ".fasta" files (mode: folder)
    :param ans_dir: directory with edited ".fasta" files
    :param hinge_file_path: path to hinge file
    :param prefix: prefix for edited files(in ans_dir)
    :param min_len: minimum length of read(in task_dir)
    :param pattern: pattern for sequences which need to process
    :param task_file: task ".fasta" file (mode: file)
    :return:
    """
    make_dir(ans_dir + "\cash")  # creating directory for cash files
    cash_dir = ans_dir + "\cash"
    if task_file:  # mode: file
        for i in tqdm(range(1)):
            ans_path_long = path.join(ans_dir, prefix + "_long" + "_" + str(i + 1) + ".fasta")
            ans_path_short = path.join(ans_dir, prefix + "_short" + "_" + str(i + 1) + ".fasta")

            cash_path = path.join(cash_dir, prefix + "_cash" + "_" + str(i + 1) + ".fasta")

            data_file = FastaFile(task_file, min_len)
            res_file = ResFastaFile(hinge_file_path, data_file)

            res_file.correct_lines(pattern)
            res_file.write_data(ans_path_long, ans_path_short, cash_path)

    else:  # mode: folder
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
            class FastaFile
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
        def add_hinge(name, line):
            """
            :param line: seq like ...PATTERN
            :param name: name of line

            hinge: [seq1, seq2, ...]
            names: [name + 1, name + 2, ...]
            lines: [seq + se1, seq + seq2, ...]
            """
            names = [name + " " + str(k) for k in range(1, len(self.hinge) + 1)]
            lines = [line + h for h in self.hinge]

            return names, lines
        # short reads
        for i in range(len(self.data.reads_short)):
            read_s = self.data.reads_short[i]
            if re.search(pattern, read_s):
                line = re.search(pattern, read_s).group(0)
                names_s, lines_s = add_hinge(self.data.names_short[i], line)
                self.new_names_short.append(names_s)
                self.lines_short.append(lines_s)

            else:  # nothing found
                self.cash_lines.append(read_s)
                self.cash_names.append(self.data.names_short[i])

        # long reads
        for i in range(len(self.data.reads_long)):
            read_l = self.data.reads_long[i]
            if re.search(pattern, read_l):
                line = re.search(pattern, read_l).group(0)
                names_l, lines_l = add_hinge(self.data.names_long[i], line)
                self.new_names.append(names_l)
                self.lines.append(lines_l)

            else:  # nothing found
                self.cash_lines.append(read_l)
                self.cash_names.append(self.data.names_long[i])

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
