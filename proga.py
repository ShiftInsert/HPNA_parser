import sys
from PyQt5.QtWidgets import QWidget, QLineEdit, QGridLayout, QApplication, QPushButton, QFileDialog, QPlainTextEdit, QLabel
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QStatusBar

from white_black_list import filter_by_number, config_init


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        ''' Setting up grid, fields to enter data.
            self.path           - path to file
            self.neededcolumns  - collumns for parsed report
            self.columnparse    - collumn to parse data
            self.delimeter      - delimeter
            self.blacklist      - blacklist
            self.whitelist      - whitelist
            self.search         - search pattern
            self.replace        - replace pattern
        '''
        self.font_size_m = 10
        self.font_size_s = 8
# Setting up the GUI grid
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setColumnStretch(0, 4)
        grid.setColumnStretch(1, 4)
        grid.setColumnStretch(2, 4)
        grid.setColumnStretch(3, 4)
        self.setLayout(grid)
        self.setGeometry(400, 300, 750, 300)                            # установка окна
        self.setWindowTitle('CSV parser')
# File path label and field
        self.pathLabel = QLabel(self)
        self.pathLabel.setText('Path to file:')
        grid.addWidget(self.pathLabel, 0, 0)
        font = self.pathLabel.font()  # lineedit current font
        font.setPointSize(self.font_size_s)  # change it's size
        self.pathLabel.setFont(font)  # set font

        self.path = QLineEdit()
        self.path.setPlaceholderText("Path to source file:")
        font = self.path.font()  # lineedit current font
        font.setPointSize(self.font_size_m)  # change it's size
        self.path.setFont(font)  # set font
        grid.addWidget(self.path,1,0,1,3)
# Open file button
        self.btnopen = QPushButton('Open', self)
        font = self.btnopen.font()  # lineedit current font
        font.setPointSize(self.font_size_m)  # change it's size
        self.btnopen.setFont(font)  # set font
        grid.addWidget(self.btnopen, 1, 3)
        self.btnopen.clicked.connect(self.openFileNameDialog)           # connect procedure to button
# Needed columns label and field
        self.neededcolumnsLabel = QLabel(self)
        self.neededcolumnsLabel.setText('Needed columns:')
        grid.addWidget(self.neededcolumnsLabel, 2, 0)
        font = self.neededcolumnsLabel.font()  # lineedit current font
        font.setPointSize(self.font_size_s)  # change it's size
        self.neededcolumnsLabel.setFont(font)  # set font

        self.neededcolumns = QLineEdit()
        self.neededcolumns.setPlaceholderText("2 3 9")
        font = self.neededcolumns.font()  # lineedit current font
        font.setPointSize(self.font_size_m)  # change it's size
        self.neededcolumns.setFont(font)  # set font
        grid.addWidget(self.neededcolumns, 3, 0, 1, 1)
# 'Column to parse' label & field
        self.columnparseLabel = QLabel(self)
        self.columnparseLabel.setText('Column to parse:')
        grid.addWidget(self.columnparseLabel, 2, 2)
        font = self.columnparseLabel.font()  # lineedit current font
        font.setPointSize(self.font_size_s)  # change it's size
        self.columnparseLabel.setFont(font)  # set font

        self.columnparse = QLineEdit()
        self.columnparse.setPlaceholderText("9")
        font = self.columnparse.font()  # lineedit current font
        font.setPointSize(self.font_size_m)  # change it's size
        self.columnparse.setFont(font)  # set font
        grid.addWidget(self.columnparse, 3, 2)
# Delimiter label & field
        self.delimeterLabel = QLabel(self)
        self.delimeterLabel.setText('Delimiter:')
        grid.addWidget(self.delimeterLabel, 2, 3)
        font = self.delimeterLabel.font()  # lineedit current font
        font.setPointSize(self.font_size_s)  # change it's size
        self.delimeterLabel.setFont(font)  # set font
        
        self.delimiter = QLineEdit()
        self.delimiter.setPlaceholderText(",")
        font = self.path.font()  # lineedit current font
        font.setPointSize(self.font_size_m)  # change it's size
        self.path.setFont(font)  # set font
        self.delimiter.setAlignment(Qt.AlignCenter)
        grid.addWidget(self.delimiter, 3, 3)
# White list label & field
        self.whitelistLabel = QLabel(self)
        self.whitelistLabel.setText('Whitelist regex: (all lines with this content will stay, empty whitelist = all lines will stay)')
        grid.addWidget(self.whitelistLabel, 4, 0)
        font = self.whitelistLabel.font()  # lineedit current font
        font.setPointSize(self.font_size_s)  # change it's size
        self.whitelistLabel.setFont(font)  # set font

        self.whitelist = QPlainTextEdit()
        self.whitelist.setTabChangesFocus(True)
        self.whitelist.setPlaceholderText("Examples:\nResult")
        font = self.whitelist.font()  # lineedit current font
        font.setPointSize(self.font_size_m)  # change it's size
        self.whitelist.setFont(font)  # set font
        grid.addWidget(self.whitelist, 5, 0, 1, 4)
# Black list label & field
        self.blacklistLabel = QLabel(self)
        self.blacklistLabel.setText('Blacklist regex: (all lines with this content will disappear)')
        grid.addWidget(self.blacklistLabel, 6, 0)
        font = self.blacklistLabel.font()  # lineedit current font
        font.setPointSize(self.font_size_s)  # change it's size
        self.blacklistLabel.setFont(font)  # set font
        
        self.blacklist = QPlainTextEdit()
        self.blacklist.setTabChangesFocus(True)
        self.blacklist.setPlaceholderText("Examples:\n^$\nResults:")
        font = self.blacklist.font()  # lineedit current font
        font.setPointSize(self.font_size_m)  # change it's size
        self.blacklist.setFont(font)  # set font
        grid.addWidget(self.blacklist, 7, 0, 1, 4)
# Search label & field
        self.searchLabel = QLabel(self)
        self.searchLabel.setText('Search regex:')
        grid.addWidget(self.searchLabel, 8, 0)
        font = self.searchLabel.font()  # lineedit current font
        font.setPointSize(self.font_size_s)  # change it's size
        self.searchLabel.setFont(font)  # set font

        self.search = QPlainTextEdit()
        self.search.setTabChangesFocus(True)
        self.search.setPlaceholderText("!!!!")
        font = self.search.font()  # lineedit current font
        font.setPointSize(self.font_size_m)  # change it's size
        self.search.setFont(font)  # set font
        grid.addWidget(self.search, 9, 0, 2, 2)
# Replace label & field
        self.replaceLabel = QLabel(self)
        self.replaceLabel.setText('Replace regex:')
        grid.addWidget(self.replaceLabel, 8, 2)
        font = self.replaceLabel.font()  # lineedit current font
        font.setPointSize(self.font_size_s)  # change it's size
        self.replaceLabel.setFont(font)  # set font

        self.replace = QPlainTextEdit()
        self.replace.setTabChangesFocus(True)
        self.replace.setPlaceholderText("????")
        font = self.replace.font()  # lineedit current font
        font.setPointSize(self.font_size_m)  # change it's size
        self.replace.setFont(font)  # set font
        grid.addWidget(self.replace, 9, 2, 2, 2)
# Run button
        self.btnrun = QPushButton('Run', self)
        font = self.btnrun.font()  # lineedit current font
        font.setPointSize(self.font_size_m)  # change it's size
        self.btnrun.setFont(font)  # set font
        grid.addWidget(self.btnrun, 12, 2)
# connect procedure to button
        self.btnrun.clicked.connect(self.parser)
        if self.path.text() == '':
            self.btnrun.setEnabled(False)
# Exit button
        self.btnexit = QPushButton('Exit', self)
        font = self.btnexit.font()  # lineedit current font
        font.setPointSize(self.font_size_m)  # change it's size
        self.btnexit.setFont(font)  # set font
        grid.addWidget(self.btnexit, 12, 3)
        self.btnexit.clicked.connect(QCoreApplication.instance().quit)

        self.statusbar = QStatusBar(self)
        self.statusbar.showMessage('READY')
        grid.addWidget(self.statusbar, 13, 0, 1, 4)
# Initializing GUI fields from config.ini
        self.yaml_config = config_init('r')
        if isinstance(self.yaml_config, dict):
            self.path.setText(self.yaml_config['input_file'])
            self.neededcolumns.setText(self.yaml_config['needed_cols'])
            self.columnparse.setText(self.yaml_config['col_to_parse'])
            self.delimiter.setText(self.yaml_config['delimit'])
            self.whitelist.setPlainText("\n".join(self.yaml_config['whitelist']))
            self.blacklist.setPlainText("\n".join(self.yaml_config['blacklist']))
            self.search.setPlainText(self.yaml_config['search_pattern'])
            self.replace.setPlainText(self.yaml_config['replace_pattern'])
        else:
            self.statusbar.showMessage(self.yaml_config)
        
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getOpenFileName(self, "Open file to parse", "", "CSV file(*.csv)", options=options)
        if filePath:
            self.fileName = filePath.split("/")[-1]
            print(self.fileName)
            self.path.setText(filePath)
            self.btnrun.setEnabled(True)
            self.statusbar.showMessage('READY')

    def parser(self):
        self.yaml_config = {
            'input_file': self.path.text(),
            'delimit': self.delimiter.text(),
            'needed_cols': self.neededcolumns.text(),
            'col_to_parse': self.columnparse.text(),
            'whitelist': self.whitelist.toPlainText().splitlines(),
            'blacklist': self.blacklist.toPlainText().splitlines(),
            'search_pattern': self.search.toPlainText(),
            'replace_pattern': self.replace.toPlainText(),
            'duplicate': False
        }
        self.statusbar.showMessage('SAVING CONFIG...')
        config_init('w', self.yaml_config)
        self.statusbar.showMessage('PARSING CSV...')
        filter_by_number(**self.yaml_config)
        self.statusbar.showMessage('JOB COMPLETE')
        print('Done')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())