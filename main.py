import sys
import time
import os.path
import subprocess
from PyQt5.QtWidgets import QWidget, QLineEdit, QGridLayout, QApplication, QPushButton, QFileDialog, QPlainTextEdit, \
    QLabel, QCheckBox, QStatusBar, QHBoxLayout, QToolTip
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QFont
from white_black_list import col_num_parser
from config_rw import config_init
from config_rw import config_w

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        ''' Setting up grid, fields to enter data.
            self.path           - path to file
            self.neededcolumns  - columns for parsed report
            self.columnparse    - column to parse data
            self.delimeter      - delimeter
            self.blacklist      - blacklist
            self.whitelist      - whitelist
            self.search         - search pattern
            self.replace        - replace pattern
        '''
        QToolTip.setFont(QFont('Consolas', 12))
        self.yaml_config, self.status_message = config_init()
        self.dupecheckstate = self.yaml_config['duplicate']
        self.font_size_m = 12
        self.font_size_s = 10
        self.currentRow = 0
        # Setting up the GUI grid
        grid = QGridLayout()
        grid.setSpacing(10)
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
        self.path.setToolTip("Either a full path to the source file, e.g.:\nC:\Downloads\MY PROJECTS\VLAN CLEANUP\\test.csv\nor just a file name if it's in the same folder with this .exe:\ntest.csv")
        self.path.setToolTipDuration(60000)
        self.path.setPlaceholderText("Path to source file:")
        font = self.path.font()  
        font.setPointSize(self.font_size_m)  
        self.path.setFont(font)  
        grid.addWidget(self.path, self.currentRow, 0, 1, 3)
        # Open file button
        self.btnopen = QPushButton('Open', self)
        self.btnopen.setFixedWidth(100)
        font = self.btnopen.font()  
        font.setPointSize(self.font_size_m)  
        self.btnopen.setFont(font)  
        grid.addWidget(self.btnopen, self.currentRow, 3)
        self.btnopen.clicked.connect(self.openFileNameDialog)  # connect procedure to button
        # Show file button
        self.btnopen = QPushButton('Open', self)
        self.btnopen.setFixedWidth(100)
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
        self.dupecheckboxLabel = QLabel(self)
        self.dupecheckboxLabel.setText('Repeat mode')
        grid.addWidget(self.dupecheckboxLabel, self.currentRow, 3)
        font = self.dupecheckboxLabel.font()
        font.setPointSize(self.font_size_s)
        self.dupecheckboxLabel.setFont(font)
        self.currentRow += 1
        # Needed columns field
        self.neededcolumns = QLineEdit()
        self.neededcolumns.setPlaceholderText("B C I")
        font = self.neededcolumns.font()  
        font.setPointSize(self.font_size_m)  
        self.neededcolumns.setFont(font)  
        grid.addWidget(self.neededcolumns, self.currentRow, 0, 1, 1)
        self.neededcolumns.setToolTip("Enter column names that you want to leave, space separated.\nFor HPNA report it's usually C for switch name and I for script output, so:\nC I")
        self.neededcolumns.setToolTipDuration(60000)
        # Delimiter field
        self.delimiter = QLineEdit()
        self.delimiter.setPlaceholderText(",")
        font = self.delimiter.font()
        font.setPointSize(self.font_size_m)
        self.delimiter.setFont(font)
        self.delimiter.setAlignment(Qt.AlignCenter)
        grid.addWidget(self.delimiter, self.currentRow, 1)
        self.delimiter.setToolTip("Enter delimiter used in the source file\nHPNA reports are comma separated, so:\n,")
        self.delimiter.setToolTipDuration(60000)
        # 'Column to parse' field
        self.columnparse = QLineEdit()
        self.columnparse.setPlaceholderText("I")
        font = self.columnparse.font()  
        font.setPointSize(self.font_size_m)  
        self.columnparse.setFont(font)  
        grid.addWidget(self.columnparse, self.currentRow, 2)
        self.columnparse.setToolTip("Enter column name with the HPNA script output for each switch\nUsually it's \"I\" column, so:\nI")
        self.columnparse.setToolTipDuration(60000)
        # 'Duplicate unparsed:' field
        self.dupecheckbox = QCheckBox('', self)
        # self.dupecheckbox.toggle()
        self.dupecheckbox.stateChanged.connect(self.do_dupecheck)
        grid.addWidget(self.dupecheckbox, self.currentRow, 3)
        self.dupecheckbox.setToolTip("Repeat switch name for each line that stays in the output")
        self.dupecheckbox.setToolTipDuration(60000)
        self.currentRow += 1
        # White list label & field
        self.whitelistLabel = QLabel(self)
        self.whitelistLabel.setText(
            'Whitelist regex: (all lines with this content will stay)')
        grid.addWidget(self.whitelistLabel, self.currentRow, 0, 1, 2)
        font = self.whitelistLabel.font()  
        font.setPointSize(self.font_size_s)  
        self.whitelistLabel.setFont(font)
        self.currentRow += 1
        self.whitelist = QPlainTextEdit()
        self.whitelist.setTabChangesFocus(True)
        self.whitelist.setPlaceholderText("empty")
        font = self.whitelist.font()  
        font.setPointSize( self.font_size_m)
        self.whitelist.setFont(font)  
        grid.addWidget(self.whitelist, self.currentRow, 0, 1, 4)
        self.whitelist.setToolTip("Each line should have a separate regex, e.g.:\nResult\nARPA\n[C|c]onnected\nAny line that contains ANY of those regexes will stay\nRegex .* will keep all lines")
        self.whitelist.setToolTipDuration(60000)
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
        self.blacklist.setPlaceholderText("empty")
        font = self.blacklist.font()
        font.setPointSize(self.font_size_m)
        self.blacklist.setFont(font)
        grid.addWidget(self.blacklist, self.currentRow, 0, 1, 4)
        self.blacklist.setToolTip("Each line should have a separate regex, e.g.:\nResults:\n#\n[N|n]otconnect\nAny line that contains ANY of those regexes will be removed\nBlacklist is applied to whitelist results and may remove them!")
        self.blacklist.setToolTipDuration(60000)
        self.currentRow += 1
        # Search label
        grid2 = QGridLayout()
        self.searchLabel = QLabel(self)
        self.searchLabel.setText('Search regex:')
        grid2.addWidget(self.searchLabel, 0, 0)
        font = self.searchLabel.font()  
        font.setPointSize(self.font_size_s)  
        self.searchLabel.setFont(font)
        # Replace label
        self.replaceLabel = QLabel(self)
        self.replaceLabel.setText('Replace regex: (to replace to nothing press Enter in the replace line)')
        grid2.addWidget(self.replaceLabel, 0, 2)
        font = self.replaceLabel.font()
        font.setPointSize(self.font_size_s)
        self.replaceLabel.setFont(font)
        #self.currentRow += 1
        # Search field
        self.search = QPlainTextEdit()
        self.search.setTabChangesFocus(True)
        self.search.setPlaceholderText("empty")
        font = self.search.font()  
        font.setPointSize(self.font_size_m)  
        self.search.setFont(font)  
        grid2.addWidget(self.search, 1, 0, 1, 2)
        self.search.setToolTip("Each line should have a separate regex, e.g.:\nVlan:\n-+\n[D|d]ate\nEach search line MUST have a paired replace line.")
        self.search.setToolTipDuration(60000)
        # Replace field
        self.replace = QPlainTextEdit()
        self.replace.setTabChangesFocus(True)
        self.replace.setPlaceholderText("empty")
        font = self.replace.font()  
        font.setPointSize(self.font_size_m)  
        self.replace.setFont(font)  
        grid2.addWidget(self.replace, 1, 2, 1, 2)
        self.replace.setToolTip("Each line MUST have a separate regex paired with every search line, e.g.:\nVLAN:\n\ndate\nTo replace to nothing - use an empty string by pressing Enter.")
        self.replace.setToolTipDuration(60000)
        grid.addLayout(grid2, self.currentRow, 0, 2, 4)
        self.currentRow += 2
        # Run button
        self.btnrun = QPushButton('Run', self)
        self.btnrun.setFixedWidth(100)
        font = self.btnrun.font()
        font.setPointSize(self.font_size_m)
        self.btnrun.setFont(font)
        # connect procedure to button
        self.btnrun.clicked.connect(self.parser)
        # Show button
        self.btnshow = QPushButton('Show Result', self)
        self.btnshow.setFixedWidth(150)
        font = self.btnshow.font()
        font.setPointSize(self.font_size_m)
        self.btnshow.setFont(font)
        # connect procedure to button
        self.btnshow.clicked.connect(self.show_result)
        # Save button
        self.btnsave = QPushButton('Save Config', self)
        self.btnsave.setFixedWidth(150)
        font = self.btnsave.font()
        font.setPointSize(self.font_size_m)
        self.btnsave.setFont(font)
        # connect procedure to button
        self.btnsave.clicked.connect(self.save_config)
        # Exit button
        self.btnexit = QPushButton('Exit', self)
        self.btnexit.setFixedWidth(100)
        font = self.btnexit.font()
        font.setPointSize(self.font_size_m)  
        self.btnexit.setFont(font)  
        #grid.addWidget(self.btnexit, self.currentRow, 3)
        self.btnexit.clicked.connect(QCoreApplication.instance().quit)
        # self.btnexit.clicked.connect(self.exit_app)
        # creating additional box layout for buttons and put it in the grid
        hboxbtns = QHBoxLayout()
        hboxbtns.setSpacing(10)
        hboxbtns.addStretch(1)
        hboxbtns.addWidget(self.btnrun)
        hboxbtns.addWidget(self.btnshow)
        hboxbtns.addWidget(self.btnsave)
        hboxbtns.addWidget(self.btnexit)
        grid.addLayout(hboxbtns, self.currentRow, 2, 1, 2)
        #grid.addItem(hboxbtns, self.currentRow, 2, 1, 2)
        self.currentRow += 1
        # Status bar
        self.statusbar = QStatusBar(self)
        self.statusbar.showMessage(self.status_message)
        grid.addWidget(self.statusbar, self.currentRow, 0, 1, 4)
        
        # Initializing GUI fields from config.ini
        if self.yaml_config['input_file']:
            self.path.setText(self.yaml_config['input_file'])
        self.neededcolumns.setText(self.yaml_config['needed_cols'])
        self.columnparse.setText(self.yaml_config['col_to_parse'])
        self.delimiter.setText(self.yaml_config['delimit'])
        self.whitelist.setPlainText("\n".join(self.yaml_config['whitelist']))
        self.blacklist.setPlainText("\n".join(self.yaml_config['blacklist']))
        self.search.setPlainText(self.yaml_config['search_pattern'])
        self.replace.setPlainText(self.yaml_config['replace_pattern'])
        if self.yaml_config['duplicate']:
            self.dupecheckbox.setChecked(True)
        else:
            self.dupecheckbox.setChecked(False)
        
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Open file to parse", "", "CSV file(*.csv)", options=options)
        if filePath:
            self.fileName = filePath.split("/")[-1]
            self.path.setText(filePath)
            self.statusbar.showMessage('READY')

    def do_dupecheck(self, state):
        if state == Qt.Checked:
            self.dupecheckstate = True
        else:
            self.dupecheckstate = False

    def save_config(self):
        self.yaml_config = {
            'input_file': self.path.text(),
            'delimit': self.delimiter.text(),
            'needed_cols': self.neededcolumns.text(),
            'col_to_parse': self.columnparse.text(),
            'whitelist': self.whitelist.toPlainText().splitlines(),
            'blacklist': self.blacklist.toPlainText().splitlines(),
            'search_pattern': self.search.toPlainText(),
            'replace_pattern': self.replace.toPlainText(),
            'duplicate': self.dupecheckstate
        }
        temp_check_write_access = self.check_write_access('config.ini')
        if temp_check_write_access:
            self.statusbar.showMessage('SAVING CONFIG...')
            self.statusbar.showMessage(config_w(self.yaml_config))
        print(self.path.text())

    def check_write_access(self, f):
        try:
            os.rename(f, f)
            return True
        except PermissionError:
            return False

    
    def show_result(self):
        temp_outfile = self.path.text().split('.csv')[0] + '_out.csv'
        if os.path.isfile(temp_outfile):
            if self.check_write_access(temp_outfile):
                subprocess.Popen([temp_outfile], shell=True)
                self.statusbar.showMessage('SHOWING RESULT')
                # self.statusbar.showMessage('DONE')
                # while True:
                #     if self.check_write_access():
                #         self.statusbar.showMessage('STILL OPENING')
                #         time.sleep(1)
                #     else:
                #         self.statusbar.showMessage('DONE')
                #         break

            else:
                self.statusbar.showMessage('!!! OUTPUT FILE ALREADY OPENED !!!')
        else:
            self.statusbar.showMessage('!!! FILE NOT FOUND !!!')

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
            'duplicate': self.dupecheckstate
        }
        self.save_config()
        if self.columnparse.text() not in self.neededcolumns.text().split(' '):
            self.statusbar.showMessage('!!! WRONG COLUMN TO PARSE !!!')
            return
        temp_outfile = self.path.text().split('.csv')[0] + '_out.csv'
        if os.path.isfile(self.path.text()):
            if os.path.isfile(temp_outfile):
                write_acc_granted = self.check_write_access(temp_outfile)
                if not write_acc_granted:
                    self.statusbar.showMessage('!!! ' + temp_outfile.upper() + ' IS USED BY ANOTHER PROCESS, WRITE FAILED !!!')
                    return
            self.statusbar.showMessage('PARSING CSV...')
            parser_message = col_num_parser(**self.yaml_config)
            if parser_message:
                self.statusbar.showMessage(parser_message)
                return
            self.statusbar.showMessage('JOB COMPLETE')
            self.show_result()
        else:
            self.statusbar.showMessage('!!! SOURCE FILE NOT FOUND !!!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())