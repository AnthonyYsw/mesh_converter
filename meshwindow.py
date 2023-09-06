import os
import subprocess
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QFileDialog, QWidget, QListWidget, QGridLayout, QHBoxLayout
from createconfig import create_config
from ruleeditor import RuleEditor
from vtkconsole import VTKApp

class MeshWindow(QMainWindow):
    """
    MeshWindow appears after clicking the [Mesh Convert] button.
    It pops up a window:
        - select the grid files (*.cgns)
        - import rules and edit the rules
        - generate the "STEP-1-config.yaml"

    It may looks like
    __________________________      __________________________ 
    |                        |     |zone1.cgns                |
    |                        | <<  |zone2.cgns                |
    |                        | >>  |zone3.cgns                |
    |________________________|     |zone4.cgns________________|
    [import rules][Edit Rules]               [Save]
    """
    def __init__(self, translator, parent=None):
        super(MeshWindow, self).__init__(parent)
        self.initUI()
        self.translator = translator
        self.setGeometry(1700, 200, 200, 200)

    def initUI(self):
        layout = QGridLayout()

        # ListWidgets
        self.leftList  = QListWidget(self)
        self.rightList = QListWidget(self)

        # Ensure current directory files with .cgns extension are added
        current_directory = os.getcwd()
        for f in os.listdir(current_directory):
            if f.endswith('.cgns'):
                self.rightList.addItem(f)
                
        layout.addWidget(self.leftList, 0, 0)
        layout.addWidget(self.rightList, 0, 2)

        # Lay the buttons
        btn_layout = QVBoxLayout()
        self.btn_to_left  = QPushButton("<<", self)
        self.btn_to_right = QPushButton(">>", self)
        self.btn_to_left.clicked.connect(self.moveToLeft)
        self.btn_to_right.clicked.connect(self.moveToRight)
        btn_layout.addWidget(self.btn_to_left)
        btn_layout.addWidget(self.btn_to_right)
        layout.addLayout(btn_layout, 0, 1)

        # Control buttons lay out horizontally
        btn_layout = QHBoxLayout()
        
        self.import_rules_btn = QPushButton(self.tr("Import Rules"), self)
        self.edit_rules_btn   = QPushButton(self.tr("Edit Rules"), self)
        self.save_btn = QPushButton(self.tr("Save"), self)
        
        self.import_rules_btn.clicked.connect(self.importRules)
        self.edit_rules_btn.clicked.connect(self.openEditor)
        self.save_btn.clicked.connect(self.saveFile)
        
        btn_layout.addWidget(self.import_rules_btn)
        btn_layout.addWidget(self.edit_rules_btn)

        layout.addLayout(btn_layout, 1, 0)
        layout.addWidget(self.save_btn, 1, 2)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle(self.tr("Mesh Window"))

    ### define the control functions
    def moveToLeft(self):
        current_item = self.rightList.currentItem()
        if current_item:
            self.leftList.addItem(current_item.text())
            self.rightList.takeItem(self.rightList.row(current_item))

    def moveToRight(self):
        current_item = self.leftList.currentItem()
        if current_item:
            self.rightList.addItem(current_item.text())
            self.leftList.takeItem(self.leftList.row(current_item))

    def importRules(self):
        default_directory = "/home/anthony/Documents/123/PyQt/STEP-1/"
        file_name, _ = QFileDialog.getOpenFileName(self, self.tr("Open Rule File"), default_directory)
        if file_name:
            self.rule_file = file_name

    def saveFile(self):
        mesh_files_seq = [self.leftList.item(i).text() for i in range(self.leftList.count())]
        try:
            if hasattr(self, 'rule_file'):
                rule_file_path = self.rule_file
            else:
                rule_file_path = None
            create_config(mesh_files_seq, rule_file_path)
            self.vtk_app = VTKApp(mesh_files_seq)
        except Exception as e:
            print(f"Error: {e}")

        #source the env.sh to run the commands
        command = 'source /home/anthony/Documents/123/aesim/env.sh && \
            /home/anthony/packages/aesim_pre_gui/bin/aesim-uns-config'
        subprocess.run(command, shell=True, executable="/bin/bash")

    ### Here is the rule editor!
    def openEditor(self):
        editor = RuleEditor(self.translator)
        editor.exec_()

    def openVtkApp(self):   
        pass

    def retranslateUi(self):
        """Retranslate the UI elements to reflect the selected language."""
        
        self.setWindowTitle(self.tr("Mesh Window"))
        self.import_rules_btn.setText(self.tr("Import Rules"))
        self.edit_rules_btn.setText(self.tr("Edit Rules"))
        self.save_btn.setText(self.tr("Save"))
