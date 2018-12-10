import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, \
    QGridLayout, QLabel
# from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import pyqtSlot


class App(QDialog):
    
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 layout - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 100
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.createGridLayout()
        
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        
        self.show()
    
    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()
        self.currentRow = 0
        self.pathLabel = QLabel(self)
        self.pathLabel.setText('Path to file:')
        layout.addWidget(self.pathLabel, self.currentRow, 0, 1, 1)
        self.currentRow += 1
        layout.addWidget(QPushButton('1'), self.currentRow, 0)
        layout.addWidget(QPushButton('2'), self.currentRow, 1)
        layout.addWidget(QPushButton('3'), self.currentRow, 2)
        self.currentRow += 1
        layout.addWidget(QPushButton('4'), self.currentRow, 0)
        layout.addWidget(QPushButton('5'), self.currentRow, 1)
        layout.addWidget(QPushButton('6'), self.currentRow, 2)
        self.currentRow += 1
        layout.addWidget(QPushButton('4'), self.currentRow, 0)
        layout.addWidget(QPushButton('5'), self.currentRow, 1)
        layout.addWidget(QPushButton('6'), self.currentRow, 2)
        self.currentRow += 1
        layout.addWidget(QPushButton('7'), self.currentRow, 0)
        layout.addWidget(QPushButton('8'), self.currentRow, 1)
        layout.addWidget(QPushButton('9'), self.currentRow, 2)
        self.currentRow += 1
        layout.addWidget(QPushButton('A'), self.currentRow, 0, 1, 2)
        layout.addWidget(QPushButton('B'), self.currentRow, 2, 1, 2)
        
        self.horizontalGroupBox.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())