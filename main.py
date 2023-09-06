import sys
from PyQt5.QtWidgets import QApplication
from meshconverter import MeshConverterGUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MeshConverterGUI()
    sys.exit(app.exec_())