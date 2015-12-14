#!/usr/bin/env python2

import sys
sys.settrace
import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'
import pylab

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PySide import QtCore, QtGui

from scipy import signal


class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.R = 1
        self.L = 1
        self.C = 1

        self.sig = signal.lti([0.5], [0], 1)

        menuGroup = QtGui.QGroupBox("Options")

        filterLabel = QtGui.QLabel("Filter:")
        dropdown = QtGui.QComboBox()
        dropdown.addItem("Lowpass")
        dropdown.addItem("Highpass")
        dropdown.addItem("Bandpass")
        dropdown.addItem("Bandstop")
        self.filterType = 0 # Starting in Lowpass filter so, no capacitor


        inductorGroup = QtGui.QGroupBox("Inductor")
        self.LLineEdit = QtGui.QDoubleSpinBox()
        self.LLineEdit.setDecimals(4)
        self.LLineEdit.setValue(1)
        self.LLineEdit.setMinimum(0.0001)
        self.LLineEdit.setMaximum(100000)
        inductorLabel = QtGui.QLabel("Inductance:")

        capacitorGroup = QtGui.QGroupBox("Capacitor")
        self.CLineEdit = QtGui.QDoubleSpinBox()
        self.CLineEdit.setDecimals(4)
        self.CLineEdit.setValue(1)
        self.CLineEdit.setMinimum(0.0001)
        self.CLineEdit.setMaximum(100000)
        capacitorLabel = QtGui.QLabel("Capacitance:")

        # No capacitor in this lowpass
        self.CLineEdit.setEnabled(False)

        # Connect signals and slots
        dropdown.activated[int].connect(self.filterChanged)
        self.LLineEdit.valueChanged [float].connect(self.indChanged)
        self.CLineEdit.valueChanged [float].connect(self.capChanged)

        LLayout = QtGui.QHBoxLayout()
        LLayout.addWidget(inductorLabel,0)
        LLayout.addWidget(self.LLineEdit,1)
        inductorGroup.setLayout(LLayout)

        CLayout = QtGui.QHBoxLayout()
        CLayout.addWidget(capacitorLabel,0)
        CLayout.addWidget(self.CLineEdit,1)
        capacitorGroup.setLayout(CLayout)

        self.circuitLabel = QtGui.QLabel(self)
        self.circuit()

        menuLayout = QtGui.QVBoxLayout()
        menuLayout.addWidget(filterLabel, 0)
        menuLayout.addWidget(dropdown, 1)
        menuLayout.addWidget(inductorGroup, 2)
        menuLayout.addWidget(capacitorGroup, 3)
        menuLayout.addWidget(self.circuitLabel, 4)
        menuGroup.setLayout(menuLayout)

        self.fig = Figure(figsize=(600,600), facecolor=(1,1,1), edgecolor=(0,0,0))
        self.graphMg = self.fig.add_subplot(2,1,1,xscale='log')
        self.graphPh = self.fig.add_subplot(2,1,2,xscale='log')
        self.graphMg.set_title("Bode Diagram")
        self.graphPh.set_title("Phase Diagram")
        # generate the canvas to display the plot
        self.canvas = FigureCanvas(self.fig)
        self.plot()

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.canvas, 0)
        layout.addWidget(menuGroup, 1)
        self.setLayout(layout)

        self.setWindowTitle("Filters")

    def filterChanged(self, index):
        '''
        Self defined slot that gets called when the filter type changes
        '''
        self.filterType=index
        if index == 0:
            self.LLineEdit.setEnabled(True)
            self.CLineEdit.setEnabled(False)
            self.sig = signal.lti([0.5], [0], 1)
        elif index == 1:
            self.LLineEdit.setEnabled(False)
            self.CLineEdit.setEnabled(True)
            self.sig = signal.lti([0], [-1], 1)
        elif index == 2:
            self.LLineEdit.setEnabled(True)
            self.CLineEdit.setEnabled(True)
            self.sig = signal.lti([0], [-1j,1j], 1)
        elif index == 3:
            self.LLineEdit.setEnabled(True)
            self.CLineEdit.setEnabled(True)
            self.sig = signal.lti([-1j,1j], [0], 1)
        self.updateWindow()

    def setFunction(self):
        '''
        Set bode function from transfer function
        '''
        if self.filterType == 0:
            # -R/L
            self.sig = signal.lti(\
            [-self.R/self.L], \
            [0], \
            1)
        elif self.filterType == 1:
            # -1/RC
            self.sig = signal.lti(\
            [0], \
            [-1/(self.C*self.R)], \
            1)
        elif self.filterType == 2:
            self.sig = signal.lti(\
            [0], \
            [((-1/self.L)-(1/self.L)*(self.C-4*self.L))/2,((-1/self.L)+(1/self.L)*(self.C-4*self.L))/2], \
            1)
        elif self.filterType == 3:
            self.sig = signal.lti(\
            [(-1/self.L*self.C)**(1/2),-(-1/self.L*self.C)**(1/2)], \
            [((-1/self.L)-(1/self.L)*(self.C-4*self.L))/2,((-1/self.L)+(1/self.L)*(self.C-4*self.L))/2], \
            1)

    def indChanged(self, val):
        '''
        Self defined slot that gets called when the value of the inductor changes
        '''
        self.L = val
        self.updateWindow()

    def capChanged(self, val):
        '''
        Self defined slot that gets called when the value of the capacitor changes
        '''
        self.C = val
        self.updateWindow()

    def plot(self):
        '''
        Here goes the matplotlib magic: this function generates the Bode diagram
        '''
        w, mag, phase = signal.bode(self.sig)
        self.graphMg.clear()
        self.graphPh.clear()
        self.graphMg.plot(w, mag)
        self.graphPh.plot(w, phase, 'r')
        # FIXME: segfault on draw() under MacOSX
        # self.canvas.draw()

    def circuit(self):
        '''
        Draw the circuit as a pixmap
        '''
        if self.filterType == 0:
            pixmap = QtGui.QPixmap("Lowpass.png")
        elif self.filterType == 1:
            pixmap = QtGui.QPixmap("Hipass.png")
        elif self.filterType == 2:
            pixmap = QtGui.QPixmap("Bandpass.png")
        elif self.filterType == 3:
            pixmap = QtGui.QPixmap("Bandstop.png")
        self.circuitLabel.setPixmap(pixmap)

    def updateWindow(self):
        '''
        Update the complete window
        '''
        self.circuit()
        self.setFunction()
        self.plot()
        self.update()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
    del window
