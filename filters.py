#!/usr/bin/env python2

import sys
import matplotlib
matplotlib.use('Qt4Agg')
# matplotlib.rcParams['backend.qt4']='PySide'
import pylab

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PySide import QtCore, QtGui

class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        menuGroup = QtGui.QGroupBox("Options")

        filterLabel = QtGui.QLabel("Filter:")
        dropdown = QtGui.QComboBox()
        dropdown.addItem("Lowpass")
        dropdown.addItem("Highpass")
        dropdown.addItem("Bandpass")
        dropdown.addItem("Bandstop")

        inductorGroup = QtGui.QGroupBox("Inductor")
        self.LLineEdit = QtGui.QLineEdit()
        inductorLabel = QtGui.QLabel("Inductance:")

        capacitorGroup = QtGui.QGroupBox("Capacitor")
        self.CLineEdit = QtGui.QLineEdit()
        capacitorLabel = QtGui.QLabel("Capacitance:")

        dropdown.activated[int].connect(self.filterChanged)

        LLayout = QtGui.QHBoxLayout()
        LLayout.addWidget(inductorLabel,0)
        LLayout.addWidget(self.LLineEdit,1)
        inductorGroup.setLayout(LLayout)

        CLayout = QtGui.QHBoxLayout()
        CLayout.addWidget(capacitorLabel,0)
        CLayout.addWidget(self.CLineEdit,1)
        capacitorGroup.setLayout(CLayout)

        menuLayout = QtGui.QVBoxLayout()
        menuLayout.addWidget(filterLabel, 0)
        menuLayout.addWidget(dropdown, 1)
        menuLayout.addWidget(inductorGroup, 2)
        menuLayout.addWidget(capacitorGroup, 3)
        menuGroup.setLayout(menuLayout)

        self.plot()

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.canvas, 0)
        layout.addWidget(menuGroup, 1)
        self.setLayout(layout)

        self.setWindowTitle("Filters")

    def filterChanged(self, index):
        if index == 0:
            self.LLineEdit.setEnabled(True)
            self.CLineEdit.setEnabled(False)
        elif index == 1:
            self.LLineEdit.setEnabled(False)
            self.CLineEdit.setEnabled(True)
        elif index == 2:
            self.LLineEdit.setEnabled(True)
            self.CLineEdit.setEnabled(True)
        elif index == 3:
            self.LLineEdit.setEnabled(True)
            self.CLineEdit.setEnabled(True)

    def plot(self):

        # generate the plot
        fig = Figure(figsize=(600,600), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))
        ax = fig.add_subplot(111)
        ax.plot([0,1,3,2,2,3,4,2,1,2,3])
        # generate the canvas to display the plot
        self.canvas = FigureCanvas(fig)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
