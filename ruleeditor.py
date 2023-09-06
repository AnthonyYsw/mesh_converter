import yaml
from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QFileDialog, QWidget, QDialog, QTreeWidget, QMenu, QTreeWidgetItem, QGridLayout)
from PyQt5.QtCore import Qt

class RuleEditor(QDialog):
    """
    This is a YAML editor draft.
    Enable load, edit, and save .yaml files.
    """
    def __init__(self, translator):
        super().__init__()
        self.initUI()
        self.translator = translator

    def initUI(self):
        layout = QVBoxLayout()
        
        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels([self.tr('Attributes')])
        self.tree.itemDoubleClicked.connect(self.edit_item) #user can edit the name of elements by double-click items.

        #right-click can show the contxt menu
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)
        
        layout.addWidget(self.tree)


        btn_layout = QGridLayout()

        #load
        self.load_button = QPushButton(self.tr('Load YAML'))
        self.load_button.clicked.connect(self.load_yaml)
        btn_layout.addWidget(self.load_button, 1, 1)

        #save
        self.save_button = QPushButton(self.tr('Save YAML'))
        self.save_button.clicked.connect(self.save_yaml)
        btn_layout.addWidget(self.save_button, 0, 1)

        #collapse
        self.collapse_button = QPushButton(self.tr('Collapse All'))
        self.collapse_button.clicked.connect(self.tree.collapseAll)
        btn_layout.addWidget(self.collapse_button, 1, 0)

        #expand
        self.expand_button = QPushButton(self.tr('Expand All'))
        self.expand_button.clicked.connect(self.tree.expandAll)
        btn_layout.addWidget(self.expand_button, 0, 0)

        layout.addLayout(btn_layout)

        container = QWidget()
        container.setLayout(layout)
        layout_main = QVBoxLayout(self)
        layout_main.addWidget(container)
        
        self.setWindowTitle(self.tr('Rule Editor'))
        self.setGeometry(1950, 500, 400, 1200)
        self.setFixedSize(400,1200)

########## End of Layout ########## Start accomplishing functionalities ##########
##################################################################################
    def edit_item(self, item, column):
        """
        Enable or disable editing of the selected item in the QTreeWidget based on its content and hierarchy.

        Parameters:
        - item (QTreeWidgetItem): The item in the tree that has been double-clicked by the user.
        - column (int): The column index of the item. In this context, it's always 0 since the tree has only one column.

        Procedure:
        - Checks if the selected item has a parent and if its text matches "type" or "keywords".
        - If so, editing is prevented.
        - Otherwise, the item is made editable and editing mode is initiated for it.

        Note:
        This function is connected to the 'itemDoubleClicked' signal of the QTreeWidget, so it's called whenever an item
        in the tree is double-clicked by the user.
        """
        
        if item.parent() and (item.text(0).startswith("type") or item.text(0) == "keywords"):
            return
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.tree.editItem(item, column)

    def load_yaml(self):
        """
        Press the 'Load YAML' to select .yaml file from directory.
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load YAML File", "", "YAML Files (*.yaml *.yml);;All Files (*)", options=options)
        if not file_name:
            return

        with open(file_name, 'r') as file:
            data = yaml.safe_load(file)

        self.populate_tree(data)

    def save_yaml(self):
        """
        Save the .yaml file in the editor to a directory.
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save YAML File", "", "YAML Files (*.yaml *.yml);;All Files (*)", options=options)
        if not file_name:
            return

        data = self.tree_to_dict()

        with open(file_name, 'w') as file:
            yaml.safe_dump(data, file)

    def tree_to_dict(self):
        """
        Convert the current QTreeWidget structure into a dictionary representation.
        
        The expected tree structure is as follows:
        - Attribute (e.g., "attribute_name")
        - Type (e.g., "type type_value")
        - Keywords
            - Keyword Group (e.g., "keyword1, keyword2")
            - ...

        The resulting dictionary structure is:
        {
            "attribute_name": {
                "type": "type_value",
                "keywords": [["keyword1", "keyword2"], ...]
            },
            ...
        }

        Returns:
            dict: The dictionary representation of the QTreeWidget's structure.
        """    

        # Access the root of the tree widget
        root = self.tree.invisibleRootItem()
        data_dict = {}

        # Iterate through each attribute item in the tree
        for index in range(root.childCount()):
            attribute_item = root.child(index)
            attribute_name = attribute_item.text(0)
            attribute_data = {}

            # Iterate through child items of the current attribute (e.g., "type" and "keywords")
            for sub_index in range(attribute_item.childCount()):
                sub_item = attribute_item.child(sub_index)
                
                # If the child is of type, extract its value
                if sub_item.text(0).startswith("type"):
                    type_value = sub_item.child(0).text(0)
                    attribute_data["type"] = type_value
                # If the child represents keywords, extract the list of keywords
                elif sub_item.text(0) == "keywords":
                    keywords_list = []
                    for keyword_index in range(sub_item.childCount()):
                        keyword_item = sub_item.child(keyword_index)
                        keywords = keyword_item.text(0).split(", ")
                        keywords_list.append(keywords)
                    attribute_data["keywords"] = keywords_list

            # Add the extracted data for the current attribute to the resulting dictionary
            data_dict[attribute_name] = attribute_data

        return data_dict

########## Display the Tree Below ##########

    def populate_tree(self, data):
        """
        Populate the QTreeWidget with data from the provided dictionary.

        Parameters:
        - data (dict): A dictionary containing the data to be displayed in the tree. The structure of the dictionary
                    should be such that there's a 'type' key with a corresponding type value, and a 'keywords' key with 
                    a list of keywords as its value.

        Procedure:
        - Clears any existing items in the tree.
        - Iterates through the dictionary items.
        - For each key-value pair in the dictionary:
        - A parent tree item is created for the key.
        - A child of the parent is created to represent the 'type' of the key.
        - The type child has its own child that displays the actual type value and is editable.
        - A 'keywords' child of the parent is created.
        - Each keyword is added as a child to the 'keywords' parent.
        """

        self.tree.clear()
        for key, value in data.items():
            parent = QTreeWidgetItem(self.tree)
            parent.setText(0, key)


            type_parent = QTreeWidgetItem(parent)
            type_parent.setText(0, "type")
            # Set the flags for "type" label to be non-editable
            type_parent.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            type_child = QTreeWidgetItem(type_parent)
            type_child.setText(0, str(value['type']))
            # Set the flags for its value to be editable
            type_child.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)


            keywords_parent = QTreeWidgetItem(parent)
            keywords_parent.setText(0, 'keywords')
            for keywords in value['keywords']:
                keyword_child = QTreeWidgetItem(keywords_parent)
                keyword_child.setText(0, ", ".join(keywords))

########## Context Menu setup below ##########        

    def show_context_menu(self, position):
        item = self.tree.itemAt(position)
        context_menu = QMenu()

        if item and item.text(0) == "keywords":
            add_group_action = context_menu.addAction(self.tr("Add New Group"))
            add_group_action.triggered.connect(lambda: self.add_new_group(item))

        elif item and item.parent() and item.parent().text(0) == "keywords":
            remove_group_action = context_menu.addAction(self.tr("Remove Group"))
            remove_group_action.triggered.connect(lambda: self.remove_group(item))

        elif item and not item.parent():
            add_above_action = context_menu.addAction(self.tr("Add Attribute Above"))
            add_above_action.triggered.connect(lambda: self.add_new_attribute(item, position="above"))

            add_below_action = context_menu.addAction(self.tr("Add Attribute Below"))
            add_below_action.triggered.connect(lambda: self.add_new_attribute(item, position="below"))

            remove_action = context_menu.addAction(self.tr("Remove"))
            remove_action.triggered.connect(self.remove_item)

        context_menu.exec_(self.tree.viewport().mapToGlobal(position))

    def add_new_group(self, item):
        new_group = QTreeWidgetItem(item)
        new_group.setText(0, self.tr("New Group"))

    def add_new_attribute(self, item, position="below"):
        new_attribute = QTreeWidgetItem()
        new_attribute.setText(0, self.tr("New Attribute"))

        type_child = QTreeWidgetItem(new_attribute)
        type_child.setText(0, "type")
        # Set the flags for "type" label to be non-editable
        type_child.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        type_value_child = QTreeWidgetItem(type_child)
        type_value_child.setText(0, "1")
        # Set the flags for its value to be editable
        type_value_child.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)

        keywords_parent = QTreeWidgetItem(new_attribute)
        keywords_parent.setText(0, 'keywords')
        # Add a default empty keyword group under "keywords:"
        empty_keyword = QTreeWidgetItem(keywords_parent)
        empty_keyword.setText(0, "")

        root = self.tree.invisibleRootItem()
        if position == "above":
            index = root.indexOfChild(item)
            root.insertChild(index, new_attribute)
        else:
            index = root.indexOfChild(item) + 1
            root.insertChild(index, new_attribute)

    def remove_item(self):
        for item in self.tree.selectedItems():
            if not item.parent() or (item.parent() and not item.text(0).startswith("type") and item.text(0) != "keywords"):
                (item.parent() or self.tree.invisibleRootItem()).removeChild(item)

    def remove_group(self, item):
        item.parent().removeChild(item)

    def retranslateUi(self):
        """Retranslate the UI elements to reflect the selected language."""
        
        # Buttons
        self.load_button.setText(self.tr('Load YAML'))
        self.save_button.setText(self.tr('Save YAML'))
        self.collapse_button.setText(self.tr('Collapse All'))
        self.expand_button.setText(self.tr('Expand All'))

        # QTreeWidget Header
        self.tree.setHeaderLabels([self.tr('Attributes')])

        # Window Title
        self.setWindowTitle(self.tr('Rule Editor'))