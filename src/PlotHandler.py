import matplotlib
def ChangePlotType(type, Plot,DatasetX,DatasetY):
    if type ==1:
        if DatasetX!=None and DatasetY!=None:
            #Plot.axes.plot(DatasetX, DatasetY)
            return "Plot changed to XY."
        else:
            #Plot.axes.plot(0,0)
            return "Plot changed to XY format. No data selected."
    elif type==2:
        if DatasetX != None and DatasetY != None:
            #Plot.bar(DatasetX,DatasetY, edgecolor="white", linewidth=0.7)
            return"Plot changed to bar format."
        else:
            return "Plot changed to bar format. No data selected"

def readDataFromFile(File):
    File.read()


def PlotDataAsXY(Plot, DataX, DataY):
    Plot.axes.plot(DataX, DataY)

def PlotDataAsBarChart(Plot, DataX, DataY):
    Plot.bar(DataX, DataY, edgecolor="white", linewidth=0.7)

    