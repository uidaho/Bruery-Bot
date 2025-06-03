# Created by Phillip Boettcher on 5/8/25
# Go Vandals

import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QVBoxLayout, QSpacerItem, QSizePolicy, QPushButton
from PyQt6.QtCore import Qt

class PyQtSimple:

    def __init__(self):
        pass

    def create_window(self, window_title:str, layout_type:str, window_size:tuple):
        app = QApplication(sys.argv)
        window = QWidget()
        window.setWindowTitle(window_title)
        window.resize(window_size[0], window_size[1])
        if layout_type == 'grid':
            grid_layout = QGridLayout()
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(grid_layout)
        main_layout.setAlignment(grid_layout, Qt.AlignmentFlag.AlignCenter)

        spacer = QSpacerItem(200, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        grid_layout.addItem(spacer, 1, 3)
        grid_layout.addItem(spacer, 1, 5)



        window.setLayout(main_layout)
        return app, window, grid_layout
    
    def create_label(self, layout:QGridLayout, label:any, row:int, column:int, alignment:str = None):
        align_flag = self.determine_alignment(alignment)
        label_widget = QLabel(str(label))
        label_widget.setAlignment(align_flag)  # This sets the text alignment inside the label
        layout.addWidget(label_widget, row, column)
        return label_widget

    def create_entrybox(self, layout:QGridLayout, row:int, column:int, alignment:str=None, width:int=40, label:any=''):
        entry_box = QLineEdit()
        entry_box.setPlaceholderText(str(label))
        entry_box.setFixedWidth(width)
        layout.addWidget(entry_box, row, column, alignment=Qt.AlignmentFlag.AlignCenter)
        return entry_box
    

    def create_button(self, layout:QGridLayout, text:any, function:object, row:int, column:int, alignment:str=None):
        button = QPushButton(str(text))
        button.clicked.connect(function)
        layout.addWidget(button, row, column, alignment=Qt.AlignmentFlag.AlignCenter)
        return button

        
    def determine_alignment(self, alignment):
        if alignment is not None:
            if alignment == 'right':
                align_flag = Qt.AlignmentFlag.AlignRight
            elif alignment == 'left':
                align_flag = Qt.AlignmentFlag.AlignLeft
        else:
            align_flag = Qt.AlignmentFlag.AlignCenter
        return align_flag

