# import sys
# from PyQt5.QtWidgets import QApplication, QWidget
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#
#     w = QWidget()
#     w.resize(250, 150)
#     w.move(300, 300)
#     w.setWindowTitle('Simple')
#     w.show()
#
#     sys.exit(app.exec_())
# source = '''a
# b
# c'''
# search_pattern = ''
# replace_pattern = ''
#
# def search_and_replace(text_chunk, search_this, replace_to):
#     return text_chunk.replace(search_this, replace_to)
#
# print(search_and_replace(source, search_this, replace_to))

import yaml
from pprint import pprint
# whitelist = []
# blacklist = ['^$', 'Results:', 'Script', 'root detail', 'sh ip int b']

d = dict(p1=1, p2=2)
def f2(p1,p2):
    print (p1, p2)
f2(**d)