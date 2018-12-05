import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QApplication, QPushButton, QComboBox, QMessageBox,\
        QTextBrowser, QFileDialog, QPlainTextEdit
from PyQt5.QtCore import QCoreApplication, QFile, Qt

from white_black_list import filter_by_number


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # устнановка сетки
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.setLayout(self.grid)

        # установка окна
        self.setGeometry(400, 300, 750, 300)
        self.setWindowTitle('CSV parser')

        # подпись поля для пути к файлу
        # self.hint = QLabel('Path to file')
        # self.grid.addWidget(self.hint, 1, 0)
        # путь к файлу
        self.path = QLineEdit()
        self.path.setPlaceholderText("Path to file")
        self.grid.addWidget(self.path, 0, 0, 1, 4)
        # Needed columns
        self.neededColumns = QLineEdit()
        self.neededColumns.setPlaceholderText("Enter needed columns")
        self.grid.addWidget(self.neededColumns, 2, 0)
        # Column to parse
        self.columnParse = QLineEdit()
        self.columnParse.setPlaceholderText("Column to parse")
        self.grid.addWidget(self.columnParse, 2, 1)
        # Delimeter
        self.delimeter = QLineEdit()
        self.delimeter.setText(',')
        self.delimeter.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(self.delimeter, 2,2)
        # Black list
        self.blackList = QPlainTextEdit()
        self.blackList.setPlaceholderText("Enter Regex expression for Black List")
        self.grid.addWidget(self.blackList, 3,0,1,5)
        # White list
        self.whiteList = QPlainTextEdit()
        self.whiteList.setPlaceholderText("Enter Regex expression for White List")
        self.grid.addWidget(self.whiteList, 4, 0, 1, 5)


        # кнопка для открытия файла
        btnOpen = QPushButton('Open', self)
        self.grid.addWidget(btnOpen, 0, 4)
        # connect procedure to button
        btnOpen.clicked.connect(self.openFileNameDialog)

        # кнопка для запуска программы
        self.btnRun = QPushButton('Run', self)
        self.grid.addWidget(self.btnRun, 12, 3)
        # connect procedure to button
        self.btnRun.clicked.connect(self.parser)
        if self.path.text() == '':
            self.btnRun.setEnabled(False)

        # exit button
        btnExit = QPushButton('Exit', self)
        self.grid.addWidget(btnExit, 12, 4)
        btnExit.clicked.connect(QCoreApplication.instance().quit)

        # self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getOpenFileName(self, "Open file to parse", "", "CSV file(*.csv)", options=options)
        if filePath:
            self.fileName = filePath.split("/")[-1]
            print(self.fileName)
            self.path.setText(filePath)
            # self.path = QLineEdit(filePath)
            # self.grid.addWidget(self.path, 1, 1)
            self.btnRun.setEnabled(True)

    def parser(self):
        filter_by_number(input_file=self.path.text(), delimit=self.delimeter.text(), \
                         needed_cols=self.neededColumns.text(), col_to_parse=self.columnParse.text())
        print('Done')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

    '''test upload'''