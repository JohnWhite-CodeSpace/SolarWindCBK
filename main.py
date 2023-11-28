import os.path
import threading
import time
from pynput import keyboard
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QTextEdit, QPushButton, QFileDialog, QDialog, \
    QMenuBar, QMenu, QAction, QProgressBar
from PyQt5.QtCore import QSize, QTimer, QObject, pyqtSignal
from PyQt5.QtGui import *
import subprocess
import DataSorting as DS
import sys
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
matplotlib.use('Qt5Agg')
import PlotHandler
import DataSorting2stage as d2
from TableView import DataTableView as DTV
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parents = None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):
    update_progress_signal = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.sorted_dir = None
        self.ExtWid = None
        self.setMinimumSize(QSize(1200, 800))
        self.setWindowTitle("IBEX analizer")
        self.update_progress_signal.connect(self.update_progress)
        Startbutton = QPushButton('Start sorting data process', self)
        Startbutton.clicked.connect(self.clickStart)
        Startbutton.resize(160, 100)
        Startbutton.move(10, 40)

        Plotbutton = QPushButton('Plot data', self)
        Plotbutton.clicked.connect(self.InitDataPlotting)
        Plotbutton.resize(160, 100)
        Plotbutton.move(10, 160)

        SecondSorting = QPushButton('Second stage processing', self)
        SecondSorting.clicked.connect(self.SecondStageSorting)
        SecondSorting.resize(160,100)
        SecondSorting.move(10, 280)

        ThirdSorting = QPushButton('Collect "Good Times" data',self)
        ThirdSorting.resize(160,100)
        ThirdSorting.move(180,40)

        TermLabel = QLabel('Terminal', self)
        TermLabel.resize(200, 30)
        TermLabel.move(10, 460)

        self.Terminal = QTextEdit('', self)
        self.Terminal.resize(1180, 250)
        self.Terminal.move(10, 500)
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
        self.widget.setGeometry(350, 15, 800, 470)

        self.ProgressBar = QProgressBar(self)
        self.ProgressBar.resize(1200,15)
        self.ProgressBar.move(10,780)

        self.Progress = QLabel("Sorting progress:", self)
        self.Progress.resize(800, 30)
        self.Progress.move(10, 750)

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
        plot2action = QAction("Bar Chart",self)
        plot2action.triggered.connect(self.HandlePlot2)
        self.pitem2 = plotMenu.addAction(plot2action)
        helpMenu = menubar.addMenu("&Help")
        hitem1 = helpMenu.addAction("Open Manual")
        hitem2 = helpMenu.addAction("Open Documentation")

    def clickStart(self):
     self.Terminal.append("Choose source directory with raw data: ")
     self.source_dir = str(QFileDialog.getExistingDirectory(self, "Select Raw Data Directory"))
     self.Terminal.append(f"Chosen source: {self.source_dir}")
     self.Terminal.append("Choose directory to store sorted data:")
     self.sorted_dir = str(QFileDialog.getExistingDirectory(self, "Select Directory For Sorted Data"))
     self.Terminal.append(f"Chosen sorted directory: {self.sorted_dir}")
     threading.Thread(target=DS.InitDataFileSorting, args=(self,self.source_dir,self.sorted_dir, self.Terminal, self.Progress)).start()

    def SecondStageSorting(self):
        #print(self.sorted_dir)
        # time.sleep(2)
        self.Terminal.append("Initialising second stage of data processing...")
        self.Terminal.append("Choose storage directory for selected data sets")
        subsortdir = str(QFileDialog.getExistingDirectory(self,"Select Storage Directory"))
        self.Terminal.append("Choose directory with sorted data for further analysis:")
        self.sorted_dir = str(QFileDialog.getExistingDirectory(self,"Select Directory With Sorted Data"))
        threading.Thread(target=d2.FindCorrectDataSets, args=(self,self.sorted_dir,self.Terminal,subsortdir,self.ProgressBar,self.Progress)).start()
        #Method for selecting proper datasets
        self.Progress.setText("Sorting progress: ")
    def HandlePlot1(self):
        Datax = 0
        Datay = 0
        #self.sc.axes.cla()
        response = PlotHandler.ChangePlotType(1,None,None,None)
        threading.Thread(target=self.refresh_text_box, args=(response,)).start()
        #print("hello")
        #self.sc.draw()
    def HandlePlot2(self):
        Datax = 0
        Datay = 0
        response = PlotHandler.ChangePlotType(2, None, None, None)
        threading.Thread(target=self.refresh_text_box, args=(response,)).start()

    def refresh_text_box(self, response):
        time.sleep(0.1)  # Some delay to avoid immediate GUI updates
        self.Terminal.append(response)

    def update_progress(self, value):
        self.ProgressBar.setValue(value)
    def InitDataPlotting(self):
        plotfile = str(QFileDialog.getOpenFileName(self, "Select file to view in table:"))
        self.Terminal.append(f"Loading data from file: {os.path.abspath(plotfile)}")
        DTV.LoadDataFromFile(plotfile)
        self.Terminal.append("Data successfully loaded to IBEX Table Viewer")
        time.sleep(0.1)
        self.Terminal.append("Displaying contents in separete dialog...")
        if self.ExtWid is None:
            self.ExtWid = DTV()
        self.ExtWid.show()



def refresh_text_box(self, MYSTRING):
    self.Terminal.append('started appending %s' % MYSTRING)  # append string
    app.QApplication.processEvents()  # update gui for pyqt

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())