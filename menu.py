"""Menu Bar Section"""

import os
import pandas as pd
import numpy as np

from PyQt5 import QtWidgets as qtw
from logger import logger
# from utils.tools import open_dso, open_meter, open_proto


class MenuBarPanel:
    # setup_menu_bar# setup_menu_bar adds connections to all the menu bar options available
    def __init__(self, gui):

        self.gui = gui

        # Save action
        gui.actionSave.setShortcut("Ctrl+s")
        gui.actionSave.setStatusTip("Save File")
        gui.actionSave.triggered.connect(self.save_png)

        # Import From -> CSV action
        gui.actionImportCSV.setShortcut("Ctrl+Shift+c")
        gui.actionImportCSV.setStatusTip("Import Data from csv")
        gui.actionImportCSV.triggered.connect(self.import_csv)

        # Import From -> XLSX action
        gui.actionImportXLSX.setShortcut("Ctrl+Shift+x")
        gui.actionImportXLSX.setStatusTip("Import Data from XLSX")
        gui.actionImportXLSX.triggered.connect(self.import_xlsx)

        # Export To -> CSV action
        gui.actionExportCSV.setShortcut("Ctrl+c")
        gui.actionExportCSV.setStatusTip("Export Data into CSVs")
        gui.actionExportCSV.triggered.connect(self.save_csv)

        # Export To -> XLSX action
        gui.actionExportXLSX.setShortcut("Ctrl+x")
        gui.actionExportXLSX.setStatusTip("Export Data into xlsx")
        gui.actionExportXLSX.triggered.connect(self.save_xlsx)

        # Exit action
        gui.actionExit.setShortcut("Ctrl+q")
        gui.actionExit.setStatusTip("Exit Application")
        gui.actionExit.triggered.connect(self.exit)

    # menu bar functions

    # save_png to save the image displayed on the screen to png
    def save_png(self):
        # check if GUI has a figure and save
        if hasattr(self.gui, 'fig'):
            formats = "png (*.png);;jpeg (*.jpeg);;jpg (*.svg)"
            # collect file name using save dialog box
            name = qtw.QFileDialog.getSaveFileName(self.gui, "Save as image", "./untitled.png", formats)[0]
            if len(name) > 1:
                self.gui.fig.set_size_inches(8, 6)
                self.gui.fig.savefig(str(name), dpi=600)
                self.gui.statusbar.showMessage("Image Saved to : {} ".format(name))
        else:
            self.gui.statusbar.showMessage("Unable to Save Image : No Figure available")

    # save_csv to save data into csv
    def save_csv(self):
        logger.debug("save data into csv")
        # check is GUI has the trial_data available and save
        if hasattr(self.gui, 'trial_data'):
            formats = "csv (*.csv)"
            # collect file name using save dialog box
            name = qtw.QFileDialog.getSaveFileName(self.gui, "Export Date into CSVs", "./untitled.csv", formats)[0]
            logger.debug("file name reaceived: {}".format(name))
            if len(name) > 1:
                if ".csv" in name:
                    logger.debug("save data into file: {}".format(name))
                    for sheet, data in list(self.gui.trial_data.items()):
                        df = pd.DataFrame(data)
                        df = df.sort_index(axis=1)
                        df.to_csv(name.split('.')[0] + '-' + sheet + '.csv', index=False)

                    self.gui.statusbar.showMessage(
                        "Exported Data into : {} files".format(name.split('.')[0] + 'channel-*' + '.csv'))
        else:
            self.guistatusbar.showMessage("Unable to Export : No Raw Data Available")

    # save_xlsx to save data into xlsx
    def save_xlsx(self):
        # check is GUI has the trial_data available and save
        if hasattr(self.gui, 'trial_data'):
            formats = "xlsx (*.xlsx)"
            # collect file name using save dialog box
            name = qtw.QFileDialog.getSaveFileName(self.gui, "Export Data into XLSX", "./untitled.xlsx", formats)[0]
            if len(name) > 1:
                if ".xlsx" in name:
                    with pd.ExcelWriter(name) as writer:
                        for sheet, data in list(self.gui.trial_data.items()):
                            df = pd.DataFrame(data)
                            df = df.sort_index(axis=1)
                            df.to_excel(writer, sheet_name=sheet, index=False)

                        mode = self.gui.mode_select_tab.currentIndex()
                    self.gui.statusbar.showMessage("Exported Data into : {} ".format(name))
        else:
            self.gui.statusbar.showMessage("Unable to Export : No Trial Data Available")

    # manual_save to save the trial_date using the file_save GUI component directly
    def manual_save(self):
        logger.debug("attempting to save data")
        # check is GUI has the trial_data available and save
        if hasattr(self.gui, 'trial_data'):
            name = self.gui.file_save_path_le.text()
            logger.debug("save data into file: {}".format(name))
            if ".csv" in name:
                for sheet, data in list(self.gui.trial_data.items()):
                    df = pd.DataFrame(data)
                    df = df.sort_index(axis=1)
                    df.to_csv(name.split('.')[0] + '-' + sheet + '.csv', index=False)

                self.gui.statusbar.showMessage(
                    "Exported Data into : {} files".format(name.split('.')[0] + 'channel-*' + '.csv'))
            elif ".xlsx" in name:
                with pd.ExcelWriter(name) as writer:
                    for sheet, data in list(self.gui.trial_data.items()):
                        df = pd.DataFrame(data)
                        df = df.sort_index(axis=1)
                        df.to_excel(writer, sheet_name=sheet, index=False)

                self.gui.statusbar.showMessage("Exported Data into : {} ".format(name))
        else:
            self.gui.statusbar.showMessage("Unable to Export : No Raw Data Available")

    # reset_file_path to reset the changes made in file_save_path_le component
    def reset_file_path(self):
        path = os.getcwd() + '/docs/untitled.xlsx'
        self.gui.file_save_path_le.setText(path)

    # import_csv to load data from multiple csv files
    def import_csv(self):
        formats = "csv (*.csv)"
        # collect file name using save dialog box
        file_names = qtw.QFileDialog.getOpenFileNames(self.gui, 'Import Data from CSVs', '.', formats)[0]
        self.gui.live_data = {}
        for file_name in file_names:
            # load data into data frame
            file_name = str(file_name)
            if "channel" in file_name:
                df = pd.read_csv(file_name)
                channel = "channel-{}".format(file_name.split("/")[-1].split("-")[2].split(".")[0])
                print(channel)
        self.gui.statusbar.showMessage("Import Data Successful")

    # import_xlsx to load data from xlsx file
    def import_xlsx(self):
        formats = "xlsx (*.xlsx)"
        # collect file name using save dialog box
        filename = qtw.QFileDialog.getOpenFileName(self, 'Import Data from XLSX', '.', formats)[0]
        self.gui.live_data = {}
        if filename:
            xls = pd.read_excel(filename, sheet_name=None)
            for sheet in list(xls.keys()):
                sheet = str(sheet)
                if "channel" in sheet:
                    no_of_avg = len(list(xls[sheet].keys())) - 2

                    if "Trial-Avg" in list(xls[sheet].keys()):
                        if not sheet in self.gui.live_data:
                            self.gui.live_data[sheet] = {}
                        self.gui.live_data[sheet]["AVG"] = np.array(xls[sheet]["Trial-Avg"])
                        self.gui.live_data[sheet]["visible"] = True
                        self.gui.live_data["x"] = np.array(xls[sheet]["Time(Sec)"])
                        self.gui.live_data["no_of_avg"] = no_of_avg

            # import ale data from the raw data
            self.import_ale()
            self.gui.statusbar.showMessage("Import Data Successful")
            self.gui.reconfigure_mode()

    def exit(self):
        # self.gui.close()
        pass