import sys
from PyQt5.QtWidgets import QWidget, QLineEdit, QGridLayout, QApplication, QPushButton, QFileDialog, QPlainTextEdit, \
    QLabel, QCheckBox
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
        self.currentRow = 0
        # Setting up the GUI grid
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setColumnStretch(0, 4)
        grid.setColumnStretch(1, 4)
        grid.setColumnStretch(2, 4)
        grid.setColumnStretch(3, 4)
        self.setLayout(grid)
        self.setGeometry(400, 300, 750, 300)  # установка окна
        self.setWindowTitle('CSV parser')
        # File path label and field
        self.pathLabel = QLabel(self)
        self.pathLabel.setText('Path to file:')
        grid.addWidget(self.pathLabel, self.currentRow, 0)
        font = self.pathLabel.font()  
        font.setPointSize(self.font_size_s)  
        self.pathLabel.setFont(font)  
        self.currentRow += 1
        self.path = QLineEdit()
        self.path.setPlaceholderText("Path to source file:")
        font = self.path.font()  
        font.setPointSize(self.font_size_m)  
        self.path.setFont(font)  
        grid.addWidget(self.path, self.currentRow, 0, 1, 3)
        # Open file button
        self.btnopen = QPushButton('Open', self)
        font = self.btnopen.font()  
        font.setPointSize(self.font_size_m)  
        self.btnopen.setFont(font)  
        grid.addWidget(self.btnopen, self.currentRow, 3)
        self.btnopen.clicked.connect(self.openFileNameDialog)  # connect procedure to button
        self.currentRow += 1
        # Needed columns label
        self.neededcolumnsLabel = QLabel(self)
        self.neededcolumnsLabel.setText('Needed columns:')
        grid.addWidget(self.neededcolumnsLabel, self.currentRow, 0)
        font = self.neededcolumnsLabel.font()  
        font.setPointSize(self.font_size_s)  
        self.neededcolumnsLabel.setFont(font)  
        # Delimiter label
        self.delimeterLabel = QLabel(self)
        self.delimeterLabel.setText('Delimiter:')
        grid.addWidget(self.delimeterLabel, self.currentRow, 1)
        font = self.delimeterLabel.font()
        font.setPointSize(self.font_size_s)
        self.delimeterLabel.setFont(font)
        # 'Column to parse' label
        self.columnparseLabel = QLabel(self)
        self.columnparseLabel.setText('Column to parse:')
        grid.addWidget(self.columnparseLabel, self.currentRow, 2)
        font = self.columnparseLabel.font()
        font.setPointSize(self.font_size_s)
        self.columnparseLabel.setFont(font)
        # 'Duplicate unparsed:' label
        self.dupecheckLabel = QLabel(self)
        self.dupecheckLabel.setText('Duplicate unparsed:')
        grid.addWidget(self.dupecheckLabel, self.currentRow, 3)
        font = self.dupecheckLabel.font()
        font.setPointSize(self.font_size_s)
        self.dupecheckLabel.setFont(font)
        self.currentRow += 1
        # Needed columns field
        self.neededcolumns = QLineEdit()
        self.neededcolumns.setPlaceholderText("2 3 9")
        font = self.neededcolumns.font()  
        font.setPointSize(self.font_size_m)  
        self.neededcolumns.setFont(font)  
        grid.addWidget(self.neededcolumns, self.currentRow, 0, 1, 1)
        # Delimiter field
        self.delimiter = QLineEdit()
        self.delimiter.setPlaceholderText(",")
        font = self.path.font()
        font.setPointSize(self.font_size_m)
        self.path.setFont(font)
        self.delimiter.setAlignment(Qt.AlignCenter)
        grid.addWidget(self.delimiter, self.currentRow, 1)
        # 'Column to parse' field
        self.columnparse = QLineEdit()
        self.columnparse.setPlaceholderText("9")
        font = self.columnparse.font()  
        font.setPointSize(self.font_size_m)  
        self.columnparse.setFont(font)  
        grid.addWidget(self.columnparse, self.currentRow, 2)
        # 'Duplicate unparsed:' field
        self.dupecheck = QCheckBox('', self)
        self.dupecheck.toggle()
        self.dupecheck.stateChanged.connect(self.dupechecked)
        grid.addWidget(self.dupecheck, self.currentRow, 3)
        self.currentRow += 1
        # White list label & field
        self.whitelistLabel = QLabel(self)
        self.whitelistLabel.setText(
            'Whitelist regex: (all lines with this content will stay, empty whitelist = all lines will stay)')
        grid.addWidget(self.whitelistLabel, self.currentRow, 0, 1, 2)
        font = self.whitelistLabel.font()  
        font.setPointSize(self.font_size_s)  
        self.whitelistLabel.setFont(font)
        self.currentRow += 1
        self.whitelist = QPlainTextEdit()
        self.whitelist.setTabChangesFocus(True)
        self.whitelist.setPlaceholderText("Examples:\nResult")
        font = self.whitelist.font()  
        font.setPointSize(self.font_size_m)  
        self.whitelist.setFont(font)  
        grid.addWidget(self.whitelist, self.currentRow, 0, 1, 4)
        self.currentRow += 1
        # Black list label & field
        self.blacklistLabel = QLabel(self)
        self.blacklistLabel.setText('Blacklist regex: (all lines with this content will disappear)')
        grid.addWidget(self.blacklistLabel, self.currentRow, 0)
        font = self.blacklistLabel.font()
        font.setPointSize(self.font_size_s)
        self.blacklistLabel.setFont(font)
        self.currentRow += 1
        self.blacklist = QPlainTextEdit()
        self.blacklist.setTabChangesFocus(True)
        self.blacklist.setPlaceholderText("Examples:\n^$\nResults:")
        font = self.blacklist.font()  
        font.setPointSize(self.font_size_m)  
        self.blacklist.setFont(font)  
        grid.addWidget(self.blacklist, self.currentRow, 0, 1, 4)
        self.currentRow += 1
        # Search label
        self.searchLabel = QLabel(self)
        self.searchLabel.setText('Search regex:')
        grid.addWidget(self.searchLabel, self.currentRow, 0)
        font = self.searchLabel.font()  
        font.setPointSize(self.font_size_s)  
        self.searchLabel.setFont(font)
        # Replace label
        self.replaceLabel = QLabel(self)
        self.replaceLabel.setText('Replace regex:')
        grid.addWidget(self.replaceLabel, self.currentRow, 2)
        font = self.replaceLabel.font()
        font.setPointSize(self.font_size_s)
        self.replaceLabel.setFont(font)
        self.currentRow += 1
        # Search field
        self.search = QPlainTextEdit()
        self.search.setTabChangesFocus(True)
        self.search.setPlaceholderText("!!!!")
        font = self.search.font()  
        font.setPointSize(self.font_size_m)  
        self.search.setFont(font)  
        grid.addWidget(self.search, self.currentRow, 0, 1, 2)
        # Replace field
        self.replace = QPlainTextEdit()
        self.replace.setTabChangesFocus(True)
        self.replace.setPlaceholderText("????")
        font = self.replace.font()  
        font.setPointSize(self.font_size_m)  
        self.replace.setFont(font)  
        grid.addWidget(self.replace, self.currentRow, 2, 1, 2)
        self.currentRow += 1
        # Run button
        self.btnrun = QPushButton('Run', self)
        font = self.btnrun.font()  
        font.setPointSize(self.font_size_m)  
        self.btnrun.setFont(font)  
        grid.addWidget(self.btnrun, self.currentRow, 2)
        # connect procedure to button
        self.btnrun.clicked.connect(self.parser)
        if self.path.text() == '':
            self.btnrun.setEnabled(False)
        # Exit button
        self.btnexit = QPushButton('Exit', self)
        font = self.btnexit.font()  
        font.setPointSize(self.font_size_m)  
        self.btnexit.setFont(font)  
        grid.addWidget(self.btnexit, self.currentRow, 3)
        self.btnexit.clicked.connect(QCoreApplication.instance().quit)
        self.currentRow += 1
        # Status bar
        self.statusbar = QStatusBar(self)
        self.statusbar.showMessage('READY')
        grid.addWidget(self.statusbar, self.currentRow, 0, 1, 4)
        
        # Initializing GUI fields from config.ini
        self.yaml_config = config_init('r')
        if isinstance(self.yaml_config, dict):
            if self.yaml_config['input_file']:
                self.path.setText(self.yaml_config['input_file'])
                self.btnrun.setEnabled(True)
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

    def dupechecked(self, state):
        
        if state == Qt.Checked:
            self.dupechecked = True
        else:
            self.dupechecked = False
            
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
            'duplicate': self.dupechecked
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