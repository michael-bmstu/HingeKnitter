from fasta_file import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication
import time
import gui


class FastaWindow(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # data
        self.task_path = ""
        self.task_file = ""
        self.ans_path = ""
        self.hinge_path = ""

        # mode
        self.mode = ""  # folder/file

        # Paths
        self.pushButton.clicked.connect(self.browse_task_folder)
        self.pushButton_4.clicked.connect(self.browse_res_folder)
        self.pushButton_3.clicked.connect(self.browse_hinge_file)

        # button box (ok / cancel)
        self.buttonBox.accepted.connect(self.start_script)
        self.buttonBox.rejected.connect(QCoreApplication.instance().quit)

        # radio buttons
        self.button_group = QtWidgets.QButtonGroup()
        self.button_group.addButton(self.radioButton)
        self.button_group.addButton(self.radioButton_2)

        self.button_group.buttonClicked.connect(self._on_radio_button_clicked)
        print(self.mode)
        print(self.lineEdit_2.text())

    def _on_radio_button_clicked(self, button):
        self.mode = button.text()
        print(self.mode)

    def browse_task_folder(self):
        if self.mode == "folder":
            directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose folder")
            self.label.setText(str(directory))
            self.task_path = directory
            print("task folder is:", directory)
        if self.mode == "file":
            file_path = QtWidgets.QFileDialog.getOpenFileName(self, "Choose folder")[0]
            self.label.setText(str(file_path))
            self.task_file = file_path
            print("task file is:", file_path)

    def browse_res_folder(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose folder")
        self.label_2.setText(str(directory))
        self.ans_path = directory
        print("result folder is:", directory)

    def browse_hinge_file(self):
        directory = QtWidgets.QFileDialog.getOpenFileName(self, "Choose file")[0]
        self.label_4.setText(str(directory))
        self.hinge_path = directory
        print("hinge file path is:", directory)

    def start_script(self):
        min_len = self.spinBox.value()
        prefix = self.lineEdit.text()
        pattern = "(.*" + self.lineEdit_2.text().upper() + ")"
        print("min_len is:", min_len)
        print("prefix is:", prefix)
        print("pattern:", pattern)
        dir_walker(self.task_path, self.ans_path, self.hinge_path,
                   prefix, min_len, pattern, self.task_file)
        time.sleep(2)
        QCoreApplication.instance().quit()
