# Author: Pietro Malky
# Purpose: Provide GUI for Masterlist data loader
# Date: July 22 2019

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox


import MasterlistDataHandler


class Program:
    def __init__(self, title, geometry, defaultOutputPath):

        self.master = tk.Tk()
        self.master.title(title)
        self.master.geometry(geometry)

        self.inputCSVPath = tk.StringVar(
            master=self.master, value="No file selected")

        self.inputHeaderMap = tk.StringVar(
            master=self.master, value="./header_map.json")

        self.inputTableKeys = tk.StringVar(
            master=self.master, value="./table_keys.json")

        self.outputCSVPath = tk.StringVar(
            master=self.master, value=defaultOutputPath)

    def setInputCSVPath(self):
        self.inputCSVPath.set(askopenfilename())
        print(self.inputCSVPath)

    def setInputTableKeys(self):
        self.inputTableKeys.set(askopenfilename())

    def setInputHeaderMap(self):
        self.inputHeaderMap.set(askopenfilename())

    def handleSubmit(self):
        fin_path = self.inputCSVPath.get()
        header_map_path = self.inputHeaderMap.get()
        table_keys_path = self.inputTableKeys.get()
        fout_path = self.outputCSVPath.get()

        dataLoader = MasterlistDataHandler.MasterlistDataLoader(
            fin_path, header_map_path, table_keys_path, fout_path)

        loadResult = dataLoader.run()

        if loadResult:
            messagebox.showinfo(
                "SUCCESS", "Data loaded successfully to the database")
            self.master.destroy()
        else:
            messagebox.showerror(
                "ERROR", "Data was not loaded to the database.\n\nCheck stacktrace for more info")

    def deployGUI(self):

        # labels
        tk.Label(self.master, text="Input CSV File").grid(row=0, column=0)
        tk.Label(self.master, text="Header Mapping JSON").grid(row=1, column=0)
        tk.Label(self.master, text="Table Keys JSON").grid(row=2, column=0)
        tk.Label(self.master, text="Output File Path").grid(row=3, column=0)

        # buttons + entries
        tk.Button(self.master, text="Select File",
                  command=self.setInputCSVPath).grid(row=0, column=1)
        tk.Button(self.master, text="Select File",
                  command=self.setInputHeaderMap).grid(row=1, column=1)
        tk.Button(self.master, text="Select File",
                  command=self.setInputTableKeys).grid(row=2, column=1)
        # tk.Entry(self.master).grid(row=3, column=1)

        # path displays
        tk.Label(self.master, textvariable=self.inputCSVPath).grid(
            row=0, column=2)
        tk.Label(self.master, textvariable=self.inputHeaderMap).grid(
            row=1, column=2)
        tk.Label(self.master, textvariable=self.inputTableKeys).grid(
            row=2, column=2)
        tk.Label(self.master, textvariable=self.outputCSVPath).grid(
            row=3, column=2)

        # submit button
        tk.Button(self.master, text="Submit",
                  command=self.handleSubmit).grid(row=4, column=0)

        self.master.mainloop()


Program(
    "Masterlist Data Loader",
    "800x450",
    "./DatabaseDataOut.csv"
).deployGUI()
