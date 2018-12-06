import sys
from PyQt5.QtWidgets import QWidget, QLineEdit, QGridLayout, QApplication, QPushButton, QFileDialog, QPlainTextEdit
from PyQt5.QtCore import QCoreApplication, Qt

from white_black_list import filter_by_number, config_init


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.yaml_config=config_init('r')
        self.font_size = 10
        ''' Setting up grid, fields to enter data.
            self.path           - path to file
            self.neededcolumns  - collumns for parsed report
            self.columnparse    - collumn to parse data
            self.delimeter      - delimeter
            self.blacklist      - blacklist
            self.whitelist      - whitelist
        '''
        grid = QGridLayout()                                            # установка сетки
        grid.setSpacing(10)
        self.setLayout(grid)
        self.setGeometry(400, 300, 750, 300)                            # установка окна
        self.setWindowTitle('CSV parser')

        self.path = QLineEdit()                                         # путь к файлу
        self.path.setPlaceholderText("Path to file")
        font = self.path.font()  # lineedit current font
        font.setPointSize(self.font_size)  # change it's size
        self.path.setFont(font)  # set font
        self.path.setText(self.yaml_config['input_file'])
        grid.addWidget(self.path,0,0,1,4)

        self.neededcolumns = QLineEdit()                                # Needed columns
        self.neededcolumns.setPlaceholderText("Enter needed columns")
        font = self.neededcolumns.font()  # lineedit current font
        font.setPointSize(self.font_size)  # change it's size
        self.neededcolumns.setFont(font)  # set font
        self.neededcolumns.setText(self.yaml_config['needed_cols'])
        grid.addWidget(self.neededcolumns, 2, 0)

        self.columnparse = QLineEdit()                                  # Column to parse
        self.columnparse.setPlaceholderText("Column to parse")
        font = self.columnparse.font()  # lineedit current font
        font.setPointSize(self.font_size)  # change it's size
        self.columnparse.setFont(font)  # set font
        self.columnparse.setText(self.yaml_config['col_to_parse'])
        grid.addWidget(self.columnparse, 2, 1)

        self.delimeter = QLineEdit()                                    # Delimeter
        font = self.path.font()  # lineedit current font
        font.setPointSize(self.font_size)  # change it's size
        self.path.setFont(font)  # set font
        self.delimeter.setAlignment(Qt.AlignCenter)
        self.delimeter.setText(self.yaml_config['delimit'])
        grid.addWidget(self.delimeter, 2, 2)

        self.blacklist = QPlainTextEdit()                               # Black list
        self.blacklist.setPlaceholderText("Enter Regex expression for Black List")
        font = self.blacklist.font()  # lineedit current font
        font.setPointSize(self.font_size)  # change it's size
        self.blacklist.setFont(font)  # set font
        self.blacklist.setPlainText("\n".join(self.yaml_config['blacklist']))
        grid.addWidget(self.blacklist, 3, 0, 1, 5)

        self.whitelist = QPlainTextEdit()                               # White list
        self.whitelist.setPlaceholderText("Enter Regex expression for White List")
        font = self.whitelist.font()  # lineedit current font
        font.setPointSize(self.font_size)  # change it's size
        self.whitelist.setFont(font)  # set font
        self.whitelist.setPlainText("\n".join(self.yaml_config['whitelist']))
        grid.addWidget(self.whitelist, 4, 0, 1, 5)

        self.btnopen = QPushButton('Open', self)                        # кнопка для открытия файла
        font = self.btnopen.font()  # lineedit current font
        font.setPointSize(self.font_size)  # change it's size
        self.btnopen.setFont(font)  # set font
        grid.addWidget(self.btnopen, 0, 4)
        self.btnopen.clicked.connect(self.openFileNameDialog)           # connect procedure to button

        self.btnrun = QPushButton('Run', self)                          # кнопка для запуска программы
        font = self.btnrun.font()  # lineedit current font
        font.setPointSize(self.font_size)  # change it's size
        self.btnrun.setFont(font)  # set font
        grid.addWidget(self.btnrun, 12, 3)
        
        self.btnrun.clicked.connect(self.parser)                        # connect procedure to button
        if self.path.text() == '':
            self.btnrun.setEnabled(False)

        self.btnexit = QPushButton('Exit', self)                             # exit button
        font = self.btnexit.font()  # lineedit current font
        font.setPointSize(self.font_size)  # change it's size
        self.btnexit.setFont(font)  # set font
        grid.addWidget(self.btnexit, 12, 4)
        self.btnexit.clicked.connect(QCoreApplication.instance().quit)

        # self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getOpenFileName(self, "Open file to parse", "", "CSV file(*.csv)", options=options)
        if filePath:
            self.fileName = filePath.split("/")[-1]
            print(self.fileName)
            self.path.setText(filePath)
            self.btnrun.setEnabled(True)

    def parser(self):
        self.yaml_config = {
            'input_file': self.path.text(),
            'delimit': self.delimeter.text(),
            'needed_cols': self.neededcolumns.text(),
            'col_to_parse': self.columnparse.text(),
            'whitelist': self.whitelist.toPlainText().splitlines(),
            'blacklist': self.blacklist.toPlainText().splitlines(),
            'search_pattern': '',
            'replace_pattern': '',
            'duplicate': False
        }
        config_init('w', self.yaml_config)
        filter_by_number(**self.yaml_config)
        print('Done')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())