import PlotHandler
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFrame, QWidget, QTableView
import re
class DataTableView(QWidget,QtCore.QAbstractTableModel):
    def __init__(self):
        super.__init__()
        self.setMinimumSize(600, 400)
        self.setWindowTitle("IBEX Data Viewer")

        self.TableView = QTableView
        self.TableView.setGeometry(10,10,580, 380)



    def LoadDataFromFile(self, ChosenFile):
        dataset = ChosenFile.readLines()
        for line in dataset:
            model = re.split('\s+', line)
            self.TableView.setModel(model)

