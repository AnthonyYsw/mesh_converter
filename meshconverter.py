from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QWidget,
                             QVBoxLayout, QSpacerItem, QSizePolicy, QComboBox)
from PyQt5.QtGui  import QFont
from PyQt5.QtCore import Qt, QTranslator
from meshwindow import MeshWindow
import os

class MeshConverterGUI(QMainWindow):
    """
    MeshConverterGUI is the starter window
    Inherit from QMainWindow
    """
    def __init__(self):
        super().__init__()

        self.translator = QTranslator()
        self.app = QApplication.instance()

        # Initialize window attributes to None
        self.mesh_window = None

        # UI Components
        self.initUI()

    def initUI(self): 
        """Initializes the user interface."""
        
        # Vertical layout setup
        layout = QVBoxLayout()

        # Language ComboBox setup
        self.language_combo = QComboBox(self)
        self.language_combo.addItems(["English", "中文"])
        self.language_combo.currentIndexChanged.connect(self.change_language)
        layout.addWidget(self.language_combo, 0, Qt.AlignLeft)  # Align left

        # Fonts setup
        intro_font = QFont()
        intro_font.setPointSize(10)
        button_font = QFont()
        button_font.setBold(True)

        # Central button setup for 'Mesh Convert'
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.mesh_button = QPushButton(self.tr('Mesh Convert'), self)
        self.mesh_button.setStyleSheet('font-size: 25px')
        self.mesh_button.setFont(button_font)
        self.mesh_button.setFixedSize(200, 50)
        self.mesh_button.clicked.connect(self.showMeshWindow)
        layout.addWidget(self.mesh_button, 0, Qt.AlignCenter)  # Align center horizontally

        # Intro label setup for 'Mesh Convert'
        self.mesh_intro_label = QLabel(self.tr("Starting from mesh file,\nedit boundary groups and convert to AESIN mesh format."), self)
        self.mesh_intro_label.setFont(intro_font)
        layout.addWidget(self.mesh_intro_label, 0, Qt.AlignCenter )  # Align center horizontally
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Central button setup for 'Pre Process'
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.preprocess_button = QPushButton(self.tr('Pre Process'), self)
        self.preprocess_button.setStyleSheet('font-size: 25px')
        self.preprocess_button.setFont(button_font)
        self.preprocess_button.setFixedSize(200, 50)
        self.preprocess_button.clicked.connect(self.showVTKconsole)
        layout.addWidget(self.preprocess_button, 0, Qt.AlignCenter)  # Align center horizontally

        # Intro label setup for 'Pre Process'
        self.preprocess_intro_label = QLabel(self.tr("Open AESIM format mesh file, \nsetup parameters conditions and run pre processing"), self)
        self.preprocess_intro_label.setFont(intro_font)
        layout.addWidget(self.preprocess_intro_label, 0, Qt.AlignCenter)  # Align center horizontally 
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Set layout to central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle(self.tr('Mesh Converter v0.3'))
        
        # Window properties
        self.setFixedSize(600, 400)
        self.show()

    def change_language(self, index):
        """Change the application language based on the selected index."""
        if index == 0:  # English
            self.translator.load("")  # Unload any previous translations
        elif index == 1:  # 中文
            if self.translator.load(os.getcwd()+"/languagepacks/meshconverter_CN.qm"):  # Load the Chinese translation file
                print("Translation file loaded successfully!")
            else:
                print("Failed to load the translation file!")
        self.app.installTranslator(self.translator)
        self.retranslateUi()

    def showMeshWindow(self):
        """Displays the MeshWindow."""
        
        if not self.mesh_window:
            self.mesh_window = MeshWindow(self.translator, self)
        self.mesh_window.show()

    def showVTKconsole(self):
        """Displays the vtk console"""
        pass

    def retranslateUi(self):
        """Retranslate the UI elements to reflect the selected language."""
        
        self.setWindowTitle(self.tr('Mesh Converter v0.3'))
        self.mesh_button.setText(self.tr('Mesh Convert'))
        self.mesh_intro_label.setText(self.tr("Starting from mesh file,\nedit boundary groups and convert to AESIN mesh format."))
        self.preprocess_button.setText(self.tr('Pre Process'))
        self.preprocess_intro_label.setText(self.tr("Open AESIM format mesh file, \nsetup parameters conditions and run pre processing"))
        # If MeshWindow exists, retranslate its UI
        if self.mesh_window and hasattr(self.mesh_window, 'retranslateUi'):
            self.mesh_window.retranslateUi()
