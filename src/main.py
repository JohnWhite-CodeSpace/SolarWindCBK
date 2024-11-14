import threading
import time

from matplotlib.ticker import MaxNLocator
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QTextEdit, QPushButton, QFileDialog, QMenuBar, QAction, QProgressBar
from PyQt5.QtCore import QSize, pyqtSignal
import DataSorting as DS
import sys
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
matplotlib.use('Qt5Agg')
import PlotHandler
import DataSorting2stage as d2
import TableView as tv
import DataSorting3stage as d3
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parents = None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot()
        super(MplCanvas, self).__init__(fig)

class MainWindow(QMainWindow):
    update_progress_signal = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        self.sorted_dir = None
        self.windows = None
        self.DataX = None
        self.DataY = None
        self.setMinimumSize(QSize(1200, 800))
        self.setWindowTitle("IBEX analizer")
        self.update_progress_signal.connect(self.update_progress)
        Startbutton = QPushButton('Start sorting data process', self)
        Startbutton.clicked.connect(self.clickStart)
        Startbutton.resize(160, 80)
        Startbutton.move(10, 40)

        SecondSorting = QPushButton('Second stage processing', self)
        SecondSorting.clicked.connect(self.SecondStageSorting)
        SecondSorting.resize(160,80)
        SecondSorting.move(10, 120)

        ThirdSorting = QPushButton('Collect "Good Times" data', self)
        ThirdSorting.clicked.connect(self.ThirdStageSorting)
        ThirdSorting.resize(160, 80)
        ThirdSorting.move(10, 200)

        Plotbutton = QPushButton('Open IBEX Table Viewer', self)
        Plotbutton.clicked.connect(self.InitDataPlotting)
        Plotbutton.resize(160, 80)
        Plotbutton.move(10, 280)

        PlotData = QPushButton('Plot Data', self)
        PlotData.clicked.connect(self.HandlePlot1)
        PlotData.resize(160, 80)
        PlotData.move(10, 360)

        TermLabel = QLabel('Terminal', self)
        TermLabel.resize(200, 30)
        TermLabel.move(10, 490)

        self.Terminal = QTextEdit('', self)
        self.Terminal.resize(1180, 180)
        self.Terminal.move(10, 520)
        self.Terminal.setStyleSheet("background-color : #FFFFFF")
        self.Create_MenuBar()

        self.sc = MplCanvas(self, width=8, height=6, dpi=70)
        self.sc.axes.scatter([0,1,2,3,4], [10,1,20,3,40])

        toolbar = NavigationToolbar(self.sc,self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.sc)

        self.widget = QtWidgets.QWidget(self)
        self.widget.setLayout(layout)
        self.widget.setGeometry(250, 15, 900, 500)

        self.ProgressBar = QProgressBar(self)
        self.ProgressBar.resize(1195,15)
        self.ProgressBar.move(10,730)

        self.ProgressBar2 = QProgressBar(self)
        self.ProgressBar2.resize(1195, 15)
        self.ProgressBar2.move(10, 780)

        self.Progress = QLabel("Sorting progress:", self)
        self.Progress.resize(800, 30)
        self.Progress.move(10, 700)

        self.Progress2 = QLabel("Sorting progress:", self)
        self.Progress2.resize(800, 30)
        self.Progress2.move(10, 750)


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
    def ThirdStageSorting(self):
        self.Terminal.append("Initialising third stage of data sorting...")
        self.Terminal.append("Choose storage directory for selected data sets")
        subsortdir = str(QFileDialog.getExistingDirectory(self, "Select Storage Directory"))
        if self.sorted_dir is None:
            self.sorted_dir = str(QFileDialog.getExistingDirectory(self, "Select Source Directory"))
        threading.Thread(target=d3.ProcessHiTimes, args=(self, self.Terminal, self.ProgressBar, self.Progress, self.sorted_dir, subsortdir)).start()
        threading.Thread(target=d3.ProcessLoTimes, args=(self, self.Terminal, self.ProgressBar2, self.Progress2, self.sorted_dir, subsortdir)).start()
    def HandlePlot1(self):
        if self.windows is not None:
            Datax, Datay = self.windows.GetDataset()
            self.sc.axes.cla()
            self.sc.axes.scatter(Datax, Datay)
            self.sc.axes.xaxis.set_major_locator(MaxNLocator(nbins=8))
            self.sc.axes.yaxis.set_major_locator(MaxNLocator(nbins=8))
            self.sc.axes.autoscale()
            self.sc.draw()
        else:
            self.Terminal.append("First open IBEX Table Viewer and choose data for plotting.")
    def HandlePlot2(self):
        Datax = 0
        Datay = 0
        response = PlotHandler.ChangePlotType(2, None, None, None)
        threading.Thread(target=self.refresh_text_box, args=(response,)).start()

    def refresh_text_box(self, response):
        time.sleep(0.1)  # Some delay to avoid immediate GUI updates
        self.Terminal.append(response)

    def update_progress(self, value, PBnum):
        if PBnum ==1:
            self.ProgressBar.setValue(value)
        elif PBnum ==2:
            self.ProgressBar2.setValue(value)


    def InitDataPlotting(self):
        if self.windows is None:
            self.windows = tv.DataTableView()
        self.windows.show()

def refresh_text_box(self, MYSTRING):
    self.Terminal.append('started appending %s' % MYSTRING)  # append string
    app.QApplication.processEvents()  # update gui for pyqt

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())