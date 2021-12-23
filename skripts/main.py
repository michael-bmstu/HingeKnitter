from fasta_window import *
import sys


def window():
    app = QtWidgets.QApplication(sys.argv)
    f = FastaWindow()
    f.show()
    sys.exit(app.exec_())


def console():
    task_path = input("Enter the path of the files directory -> ")
    while not is_exists_dir(task_path):
        print("This directory doesn't exist!!!\nEnter the correct path...")
        task_path = input("Enter the path of the files directory -> ")

    hinge_path = input("Enter the path of the hinge file directory -> ")

    ans_path = input("Enter the path of the directory where result files will be saved -> ")
    while task_path == ans_path:
        print("Identical directories entered\nEnter the correct directories...")
        task_path = input("Enter the path of the files directory -> ")
        ans_path = input("Enter the path of the directory where files will be saved -> ")

        while not is_exists_dir(task_path):
            print("This directory doesn't exist!!!\nEnter the correct path...")
            task_path = input("Enter the path of the files directory -> ")

    prefix = "file"
    if input("Use prefix(default: file)? [y]es / [n]o: ") == 'y':
        prefix = input("Enter prefix for files -> ")

    min_len = 90
    if input("Change min length of read(default 90)? [y]es/[n]o: ") == 'y':
        min_len = int(input("Enter the min length ==>"))
    dir_walker(task_path, ans_path, hinge_path, prefix, min_len)


def main():
    while True:
        mode = int(input("Select mode: console - 1, window - 2: "))

        if mode == 1:
            console()
            break
        elif mode == 2:
            window()
            break
        else:
            print("Incorrect mode")


if __name__ == "__main__":
    main()
