from PyQt5 import QtWidgets as qtw
from PyQt5.uic import loadUiType

import numpy as np
import pandas as pd
from scipy import interpolate

from matplotlib.pyplot import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)

from menu import MenuBarPanel

QMainWindow, Ui_MainWindow = loadUiType('vmon.ui')


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle('vmon')

        # initialize menu bar to enable data export and import
        self.menu = MenuBarPanel(self)

        self.open_btn.clicked.connect(self.open_image)
        self.clear_btn.clicked.connect(self.clear_screen)
        self.plot_cb.currentTextChanged.connect(self.reconfigure_axes)
        self.interpolate_cb.currentTextChanged.connect(self.reconfigure_axes)
        self.legend_chb.stateChanged.connect(self.reconfigure_axes)
        self.peaks_chb.stateChanged.connect(self.reconfigure_axes)

    def open_image(self):
        formats = "sheets (*.csv *.xlsx)"
        self.sheet_files = qtw.QFileDialog.getOpenFileNames(self, 'Open Sheets', '.', formats)
        self.reconfigure_axes()

    def clear_screen(self):
        # clear screen
        if hasattr(self, "fig"):
            del self.fig
        if hasattr(self, "canvas"):
            del self.canvas
        if hasattr(self, "ax"):
            self.ax.clear()
            del self.ax

        if hasattr(self, "toolbar"):
            self.screen.removeWidget(self.toolbar)
            self.toolbar.close()
            del self.toolbar
        if hasattr(self, "image"):
            self.screen.removeWidget(self.image)
            self.image.close()
            del self.image

    def get_rx_spectrum(self, file_name, interpolation="Cubic Spline"):
        # Resolution of IMon 512 USB is 0.166015625 nm = 166.015 pm
        x = np.arange(1510, 1595, 0.166015625, dtype=float)
        dx = np.arange(1510, 1595, 0.001000000, dtype=float)

        # load data into data frame
        df = pd.read_csv(file_name, dtype=float, usecols=[i for i in range(3, 515)], sep="\t", skiprows=2)
        # calculate mean of all the entries and reverse it
        mean = df.mean()[::-1]

        if interpolation == "Cubic Spline":
            # perform cublic spline interpolation
            cs = interpolate.CubicSpline(x, mean)
            dy = cs(dx)
        elif interpolation == "Linear":
            # perform cublic spline interpolation
            cs = interpolate.CubicSpline(x, mean)
            dy = cs(dx)
        else:
            pass

        return dx, dy

    def reconfigure_axes(self):
        if not hasattr(self, "fig"):
            self.fig = Figure()
        if not hasattr(self, "canvas"):
            self.canvas = FigureCanvas(self.fig)
        if not hasattr(self, "ax"):
            self.ax = self.fig.add_subplot(111)
            self.ax.clear()
        else:
            self.ax.clear()

        self.files = []
        self.peaks = []

        for sheet_file in self.sheet_files[0]:
            dx, dy = self.get_rx_spectrum(sheet_file, interpolation=self.interpolate_cb.currentText())
            self.files.append(sheet_file.split('/')[-1].split('.')[0][-4:])
            self.peaks.append(dx[dy.argmax()])
            
            plot=self.plot_cb.currentText()
            
            if plot == "Normalised":
                dy = dy / max(dy)               
            elif plot == "Desibles":
                dy = 20 * np.log(dy / max(dy))

            if self.legend_chb.isChecked():
                if self.peaks_chb.isChecked():
                    self.ax.plot(dx, dy, label=f"{sheet_file.split('/')[-1]},{dx[dy.argmax()]:.3f}")
                else:
                    self.ax.plot(dx, dy, label=f"{sheet_file.split('/')[-1]}")
            else:
                self.ax.plot(dx, dy)
            
            # self.ax.scatter(dx[ymaxp], dy[ymaxp],label = 'peak L:' + ))

        if self.plot_cb.currentText() == "Raw":
            self.ax.set_title("FBG Spectrums")
            self.ax.set_ylabel("Amplitude (AU)")
            self.ax.set_xlabel("Wavelength (nm)")
            self.ax.set_xlim(1511, 1594)

            if self.legend_chb.isChecked():
                self.ax.legend()

        if self.plot_cb.currentText() == "Normalised":
            self.ax.set_title("Normalised FBG Spectrums")
            self.ax.set_ylabel("Normalised Amplitude (AU)")
            self.ax.set_xlabel("Wavelength (nm)")
            self.ax.set_xlim(1511, 1594)
            if self.legend_chb.isChecked():
                self.ax.legend()

        if self.plot_cb.currentText() == "Peaks":
            self.ax.clear()
            self.ax.set_title("Peaks in FBG Spectrums")
            self.ax.set_ylabel("Peak Wavelength (nm)")
            self.ax.set_xlabel("Files")
            self.ax.plot(np.arange(len(self.peaks)), self.peaks)
            self.ax.plot(self.files, self.peaks)


        if self.plot_cb.currentText() == "Desibels":
            self.ax.set_title("FBG Spectrums in Desibels")
            self.ax.set_ylabel("Amplitude (dB)")
            self.ax.set_xlabel("Wavelength (nm)")
            self.ax.set_xlim(1511, 1594)
            if self.legend_chb.isChecked():
                self.ax.legend()

        self.ax.grid("True")
        
        # self.fig.subplots_adjust(top=0.921,
        #     bottom=0.123,
        #     left=0.169,
        #     right=0.972,
        #     hspace=0.2,
        #     wspace=0.2
        # )
        self.fig.tight_layout()

        if not hasattr(self, "image"):
            self.image = FigureCanvas(self.fig)
            self.screen.addWidget(self.image)

        if not hasattr(self, "toolbar"):
            self.toolbar = NavigationToolbar(self.image, self.display, coordinates=True)
            self.screen.addWidget(self.toolbar)

        self.fig.canvas.draw()
        self.statusbar.showMessage("Reconfigured Plot")
