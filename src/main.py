import threading
import time
from pynput import keyboard
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QTextEdit, QPushButton, QFileDialog, QDialog, QMenuBar, QMenu, QAction
from PyQt5.QtCore import QSize, QTimer
import subprocess
import DataSorting as DS
import sys
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
matplotlib.use('Qt5Agg')
import PlotHandler

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parents = None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(900, 600))
        self.setWindowTitle("IBEX analizer")

        Startbutton = QPushButton('Start sorting data process', self)
        Startbutton.clicked.connect(self.clickStart)
        Startbutton.resize(150, 100)
        Startbutton.move(50, 40)

        Startbutton = QPushButton('Plot data', self)
        Startbutton.clicked.connect(self.clickStart)
        Startbutton.resize(150, 100)
        Startbutton.move(50, 160)

        TermLabel = QLabel('Terminal', self)
        TermLabel.resize(150, 30)
        TermLabel.move(10, 370)

        self.Terminal = QTextEdit('', self)
        self.Terminal.resize(880, 150)
        self.Terminal.move(10, 400)
        self.Terminal.setStyleSheet("background-color : #FFFFFF")
        self.Create_MenuBar()

        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

        toolbar = NavigationToolbar(self.sc,self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.sc)

        self.widget = QtWidgets.QWidget(self)
        self.widget.setLayout(layout)
        self.widget.setGeometry(300, 10, 550, 380)

    def Create_MenuBar(self):
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)
        fileMenu = menubar.addMenu("&File")
        fitem1 = fileMenu.addAction("Open file in terminal")
        fitem2 = fileMenu.addAction("Reload interface")
        plotMenu = menubar.addMenu("&Plot")
        plot1action = QAction("&XY Plot",self)
        plot1action.triggered.connect(self.HandlePlot1)
        self.pitem1 = plotMenu.addAction(plot1action)

        pitem2 = plotMenu.addAction("Bar Chart")
        helpMenu = menubar.addMenu("&Help")
        hitem1 = helpMenu.addAction("Open Manual")
        hitem2 = helpMenu.addAction("Open Documentation")

    def clickStart(self):
     self.Terminal.append("Choose source directory with raw data: ")
     source_dir = str(QFileDialog.getExistingDirectory(self, "Select Raw Data Directory"))
     self.Terminal.append(f"Chosen source: {source_dir}")
     self.Terminal.append("Choose directory to store sorted data:")
     sorted_dir = str(QFileDialog.getExistingDirectory(self, "Select Directory For Sorted Data"))
     self.Terminal.append(f"Chosen sorted directory: {sorted_dir}")
     DS.InitDataFileSorting(source_dir,sorted_dir)



    def HandlePlot1(self):
        Datax = 0
        Datay = 0
        #self.sc.axes.cla()
        response = PlotHandler.ChangePlotType(1,None,None,None)
        threading.Thread(target=self.refresh_text_box, args=(response,)).start()
        #print("hello")
        #self.sc.draw()

    def refresh_text_box(self, response):
        time.sleep(0.1)  # Some delay to avoid immediate GUI updates
        self.Terminal.append(response)
def refresh_text_box(self, MYSTRING):
    self.Terminal.append('started appending %s' % MYSTRING)  # append string
    app.QApplication.processEvents()  # update gui for pyqt

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())