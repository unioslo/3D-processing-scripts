# Short script to use cloud compare transforms in metashape directly.
# compiled with the help of chatGPT 3.5

import re

import Metashape
from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QFileDialog, QMessageBox, QDialogButtonBox, QVBoxLayout, QDialog


# Open a dialog window and ask the user to select an input text file
app = QtWidgets.QApplication.instance()
file_path, _ = QFileDialog.getOpenFileName(None, "Select File", "", "Text Files (*.txt)")

with open(file_path, 'r', encoding='utf-8') as file:
    input_text = file.read() # Decode and convert input_text to a string


doc=Metashape.app.document
chunk=doc.chunk


# ask the user if 
scalefactor = 1

# Create a QMessageBox
msg_box = QMessageBox()

# Set the message text
msg_box.setText("Was the transform performed in mm or metres?")

# Add buttons to the message box
msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

# Set custom button text
msg_box.setButtonText(QMessageBox.Ok, "mm")
msg_box.setButtonText(QMessageBox.Cancel, "metres")

# Show the message box and wait for user input
result = msg_box.exec_()

# If the user clicked "OK"
if result == QMessageBox.Ok:
    scalefactor = 0.001
    
if result == QMessageBox.Cancel:
    scalefactor = 1

pattern = r'(-?\d+(?:\.\d+)?(?:\s+-?\d+(?:\.\d+)?){15})'
matches = re.findall(pattern, input_text, re.DOTALL)


for group in matches:
    
    group_list = [list(map(float, line.split(' '))) for line in group.split('\n')]  # Convert group lines into a list of lists

    # Multiply the last element of each sublist of the first three sublists by scalefactor
    updated_group_list = [sublist[:-1] + [sublist[-1] * scalefactor] if sublist != group_list[-1] else sublist for sublist in group_list]
    transform = Metashape.Matrix(updated_group_list)        # Turn transformation matrix into one supported by metashape

    mOrig = chunk.transform.matrix                  # get current location matrix

    chunk.transform.matrix = transform*mOrig        # apply transform

    print("-------------------")
    print("\ntransformed model space by the following matrix:\n")
    print(transform)

