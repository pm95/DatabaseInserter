# Author: Pietro Malky
# Purpose: Provide GUI for Masterlist data loader
# Date: July 22 2019

import os
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox


import Helpers


class Program:
    def __init__(self, title, geometry, defaultOutputPath):
        self.master = tk.Tk()
        self.master.title(title)
        self.master.geometry(geometry)

        self.inputCSVPath = tk.StringVar(
            master=self.master, value="No file selected")

        self.inputColumnsMapsPath = tk.StringVar(
            master=self.master, value="No file selected")

        self.inputTableKeys = tk.StringVar(
            master=self.master, value="No file selected")

        self.dbCredentialsPath = tk.StringVar(
            master=self.master, value="No file selected")

        self.outputCSVPath = tk.StringVar(
            master=self.master, value=defaultOutputPath)

        self.gotTableSchemas = False

    def setInputCSVPath(self):
        self.inputCSVPath.set(askopenfilename())
        print(self.inputCSVPath)

    def setInputColumnsMapPath(self):
        self.inputColumnsMapsPath.set(askopenfilename())
        print(self.inputColumnsMapsPath)

    def setInputTableKeys(self):
        self.inputTableKeys.set(askopenfilename())
        print(self.inputTableKeys)

    def setDbCredentialsPath(self):
        self.dbCredentialsPath.set(askopenfilename())
        print(self.dbCredentialsPath)

    def getTableSchemas(self):
        Helpers.queryGetTableSchema(
            self.inputTableKeys.get(), self.dbCredentialsPath.get())
        self.gotTableSchemas = True
        messagebox.showinfo("Table Schema Success",
                            "Imported table schema successfully!")
        print("got table schemas")

    def handleSubmit(self):
        fin_path = self.inputCSVPath.get()
        columns_map_path = self.inputColumnsMapsPath.get()
        table_keys_path = self.inputTableKeys.get()
        fout_path = self.outputCSVPath.get()
        dbCredentialsPath = self.dbCredentialsPath.get()

        if fin_path == "No file selected" or table_keys_path == "No file selected" or dbCredentialsPath == "No file selected":
            messagebox.showerror(
                "NOT EVERY INPUT FILE SELECTED", "You must select all input files before continuing")
        elif not self.gotTableSchemas:
            messagebox.showerror(
                "ERROR", "You MUST first load the table schemas and specify special column mappings (optional)")
        else:
            loadResult = Helpers.runMainHelper(
                tablesPath=table_keys_path,
                csvNoFormatPath=fin_path,
                csvFormattedPath=fout_path,
                dbCredentialsPath=dbCredentialsPath,
                columnMappingsPath=columns_map_path
            )

            if all(loadResult) == True:
                messagebox.showinfo(
                    "SUCCESS", "Data loaded successfully to the database")
                # os.remove(fout_path)
                # print("removed intermediary file successfully")
                # self.master.destroy()
            else:
                messagebox.showerror(
                    "ERROR", '\n'.join(loadResult))

    def deployGUI(self):
        # labels
        tk.Label(self.master, text="* Input CSV File").grid(
            row=0, column=0)
        tk.Label(self.master, text="Output File Path").grid(
            row=1, column=0)
        tk.Label(self.master, text="Special Column Mappings JSON").grid(
            row=2, column=0)
        tk.Label(self.master, text="* Tables Schemas JSON").grid(
            row=3, column=0)
        tk.Label(self.master, text="* Database Credentials JSON").grid(
            row=4, column=0)

        # buttons
        tk.Button(self.master, text="Select File",
                  command=self.setInputCSVPath).grid(
            row=0, column=1)
        tk.Button(self.master, text="Select File",
                  command=self.setInputColumnsMapPath).grid(
            row=2, column=1)
        tk.Button(self.master, text="Select File",
                  command=self.setInputTableKeys).grid(
            row=3, column=1)
        tk.Button(self.master, text="Select File",
                  command=self.setDbCredentialsPath).grid(
            row=4, column=1)

        # path displays
        tk.Label(self.master, textvariable=self.inputCSVPath).grid(
            row=0, column=2)
        tk.Label(self.master, textvariable=self.outputCSVPath).grid(
            row=1, column=2)
        tk.Label(self.master, textvariable=self.inputColumnsMapsPath).grid(
            row=2, column=2)
        tk.Button(
            self.master,
            text="Query Table Schemas",
            command=self.getTableSchemas
        ).grid(row=3, column=2)
        tk.Label(self.master, textvariable=self.inputTableKeys).grid(
            row=3, column=3)
        tk.Label(self.master, textvariable=self.dbCredentialsPath).grid(
            row=4, column=2)

        # submit button
        tk.Button(
            self.master,
            text="Submit",
            command=self.handleSubmit
        ).grid(row=5, column=0)

        # misc legend
        tk.Label(self.master, text="* = mandatory file").grid(row=7, column=0)

        self.master.mainloop()


Program(
    "Masterlist Data Loader",
    "800x450",
    "./DatabaseDataOut.csv"
).deployGUI()
