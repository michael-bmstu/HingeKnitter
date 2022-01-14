from fasta_window import *
import sys


def window():
    app = QtWidgets.QApplication(sys.argv)
    f = FastaWindow()
    f.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    window()
