import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import *
import pkg_resources
import json
import subprocess

class jsonCreator:
    def __init__(self, window, importJson):
            self.window = window
            self.importJson = importJson

            self.canvas = tk.Canvas(self.window, width=420, height=700, scrollregion=(0,0,420,700), highlightthickness=0)
            self.canvas.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
            self.canvas.pack(fill=tk.BOTH)
            self.scrollbar = ttk.Scrollbar(self.window, orient="vertical",command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.scrollbar.set)
            self.scrollbar.place(relx=1,rely=0,relheight=1,anchor="ne")
            self.frame = tk.Frame(self.canvas)
            self.frame.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
            self.canvas.create_window((0, 0), window=self.frame, anchor=tk.NW)

            self.canvasLength = 700

            menubar = tk.Menu(self.window)
            self.window.config(menu=menubar)

            filemenu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="File", menu=filemenu)

            filemenu.add_command(label="Export", command=self.exportJson)

            helpmenu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Help", menu=helpmenu)

            helpmenu.add_command(label="Examples", command=self.helpMenu)

            self.entriesList = {}
            self.entryCount = 0
            self.valueCountList= []

            self.addBtn = ttk.Button(self.frame, text="+", width=2, command=lambda: self.addEntry(self.addBtn))
            self.addBtn.pack(padx=200, pady=15)

    def exportJson(self, save=True):
        self.entriesListExport = {}
        for entry in self.entriesList:
            currentEntry = self.entriesList[entry]
            if currentEntry['dataType'] == "Double Value":
                obj = {"dataType": "OnOrOffV"}
                vars = {}
                winversList = []
                varCount = 1
                for i in currentEntry:
                    widget = currentEntry[i]
                    
                    if type(widget) is str or type(widget) is ttk.Label or type(widget) is ttk.Frame or type(widget) is tk.Frame or type(widget) is ttk.Radiobutton or type(widget) is ttk.Checkbutton:
                        pass
                    elif type(widget) is ttk.Entry:
                        if varCount == 1:
                            obj["displayname"] = widget.get()
                        elif varCount == 2:
                            obj["description"] = widget.get()
                        elif varCount == 8:
                            obj["key"] = widget.get()
                        elif varCount == 9:
                            obj["value"] = widget.get()
                        elif varCount == 10:
                            obj["type"] = widget.get()
                        elif varCount == 11:
                            vars["enabled"] = widget.get()
                        elif varCount == 12:
                            vars["disabled"] = widget.get()
                            obj["values"] = vars
                        varCount += 1
                    elif type(widget) is tk.IntVar:
                        if varCount == 3:
                            if widget.get() == 1:
                                winversList.append("11")
                        elif varCount == 4:
                            if widget.get() == 1:
                                winversList.append("10")
                        elif varCount == 5:
                            if widget.get() == 1:
                                winversList.append("8.1")
                        elif varCount == 6:
                            if widget.get() == 1:
                                winversList.append("8")
                        elif varCount == 7:
                            if widget.get() == 1:
                                winversList.append("7")
                            obj["winversions"] = winversList
                        varCount += 1
            elif currentEntry['dataType'] == "Multi Value":
                obj = {"dataType": "OnOrOffMV"}
                vars = {}
                winversList = []
                varCount = 1
                switch=0
                for i in currentEntry:
                    widget = currentEntry[i]
                    if type(widget) is str or type(widget) is ttk.Label or type(widget) is ttk.Frame or type(widget) is tk.Frame or type(widget) is ttk.Radiobutton or type(widget) is ttk.Checkbutton or type(widget) is ttk.Button:
                        pass
                    elif type(widget) is ttk.Entry:
                        if varCount == 1:
                            obj["displayname"] = widget.get()
                        elif varCount == 2:
                            obj["description"] = widget.get()
                        elif varCount == 8:
                            obj["key"] = widget.get()
                        elif varCount == 9:
                            obj["value"] = widget.get()
                        elif varCount == 10:
                            obj["type"] = widget.get()
                        varCount += 1
                    elif type(widget) is tk.IntVar:
                        if varCount == 3:
                            if widget.get() == 1:
                                winversList.append("11")
                        elif varCount == 4:
                            if widget.get() == 1:
                                winversList.append("10")
                        elif varCount == 5:
                            if widget.get() == 1:
                                winversList.append("8.1")
                        elif varCount == 6:
                            if widget.get() == 1:
                                winversList.append("8")
                        elif varCount == 7:
                            if widget.get() == 1:
                                winversList.append("7")
                            obj["winversions"] = winversList
                        varCount += 1
                    elif type(widget) is dict:
                        entryText = None
                        dataValue = None
                        for i in widget:
                            subwidget = widget[i]
                            if type(subwidget) is ttk.Frame or type(subwidget) is ttk.Label:
                                pass
                            elif type(subwidget) is ttk.Entry:
                                if switch == 0:
                                    entryText = subwidget.get()
                                    switch += 1
                                elif switch == 1:
                                    dataValue = subwidget.get()
                                    vars[entryText] = dataValue
                                    switch -= 1
                        obj["values"] = vars

            elif currentEntry['dataType'] == "Key": 
                obj = {"dataType": "OnOrOffK"}
                vars = {}
                winversList = []
                varCount = 1
                for i in currentEntry:
                    widget = currentEntry[i]
                    
                    if type(widget) is str or type(widget) is ttk.Label or type(widget) is ttk.Frame or type(widget) is tk.Frame or type(widget) is ttk.Radiobutton or type(widget) is ttk.Checkbutton:
                        pass
                    elif type(widget) is ttk.Entry:
                        if varCount == 1:
                            obj["displayname"] = widget.get()
                        elif varCount == 2:
                            obj["description"] = widget.get()
                        elif varCount == 8:
                            obj["key"] = widget.get()
                        varCount += 1
                    elif type(widget) is tk.IntVar:
                        if varCount == 3:
                            if widget.get() == 1:
                                winversList.append("11")
                        elif varCount == 4:
                            if widget.get() == 1:
                                winversList.append("10")
                        elif varCount == 5:
                            if widget.get() == 1:
                                winversList.append("8.1")
                        elif varCount == 6:
                            if widget.get() == 1:
                                winversList.append("8")
                        elif varCount == 7:
                            if widget.get() == 1:
                                winversList.append("7")
                            obj["winversions"] = winversList
                        elif varCount == 9:
                                print("reached")
                                if widget.get() == 1:
                                    vars["enabled"] - "Create the key"
                                    vars["disabled"] = "Delete the key"
                                    obj["values"] = vars
                                if widget.get() == 0:
                                    vars["enabled"] = "Delete the key"
                                    vars["disabled"] = "Create the key"
                                    obj["values"] = vars
                        varCount += 1
            elif currentEntry['dataType'] == "String":
                obj = {"dataType": "String"}
                winversList = []
                varCount = 1
                for i in currentEntry:
                    widget = currentEntry[i]
                    
                    if type(widget) is str or type(widget) is ttk.Label or type(widget) is ttk.Frame or type(widget) is tk.Frame or type(widget) is ttk.Radiobutton or type(widget) is ttk.Checkbutton:
                        pass
                    elif type(widget) is ttk.Entry:
                        if varCount == 1:
                            obj["displayname"] = widget.get()
                        elif varCount == 2:
                            obj["description"] = widget.get()
                        elif varCount == 8:
                            obj["key"] = widget.get()
                        elif varCount == 9:
                            obj["value"] = widget.get()
                        elif varCount == 10:
                            obj["type"] = widget.get()
                        elif varCount == 11:
                            obj["DefaultValue"] = widget.get()
                        varCount += 1
                    elif type(widget) is tk.IntVar:
                        if varCount == 3:
                            if widget.get() == 1:
                                winversList.append("11")
                        elif varCount == 4:
                            if widget.get() == 1:
                                winversList.append("10")
                        elif varCount == 5:
                            if widget.get() == 1:
                                winversList.append("8.1")
                        elif varCount == 6:
                            if widget.get() == 1:
                                winversList.append("8")
                        elif varCount == 7:
                            if widget.get() == 1:
                                winversList.append("7")
                            obj["winversions"] = winversList
                        varCount += 1
            self.entriesListExport[entry] = obj
        if save:
            var = subprocess.check_output("powershell \"[Environment]::GetFolderPath('Desktop')\"", shell=True)
            path = asksaveasfilename(title="Export JSON data", defaultextension=".json", initialdir=str(var.decode('utf-8')), initialfile="keys.json", filetypes=[("JSON files", "*.json"), ("All Files", "*.*")])
            jsonData = json.dumps(self.entriesListExport, indent=3)
        if path:
            with open(path, "w") as file:
                file.write(jsonData)  
        else:
            return jsonData

    def addEntry(self, addBtn):
        addBtn.forget()
        dataTypes = ("Double Value", "Multi Value", "Key", "String")
        def addEntryFull(self, dataType, entryIndex, subframe, rSet, addBtn, entryIndexText):
            def changeEntryDataType(self, entryIndex, addBtn):
                addBtn.forget()
                passedInframe=0
                passedIndexText=0
                for widgetI in self.entriesList[f"{entryIndex}"]:
                    widget = self.entriesList[f"{entryIndex}"][f"{widgetI}"]
                    NoneType = type(None)
                    if type(widget) is ttk.Frame and passedInframe < 2:
                        passedInframe+=1
                    elif type(widget) is ttk.Label and passedIndexText < 1:
                        passedIndexText+=1
                    elif type(widget) is ttk.Radiobutton or type(widget) is tk.IntVar or type(widget) is NoneType or type(widget) is str:
                        pass
                    else:
                        if type(widget) == dict:
                            for subwidget in widget:
                                widget[str(subwidget)].destroy()
                        else:
                            widget.destroy()
                    
            changeEntryDataType(self, entryIndex, addBtn)
            if dataType == "Double Value":
                displaynameFrame = ttk.Frame(subframe)
                displaynameText = ttk.Label(displaynameFrame, text="Display name: ")
                displaynameEntry = ttk.Entry(displaynameFrame, width=40)
                descriptionFrame = ttk.Frame(subframe)
                descriptionText = ttk.Label(descriptionFrame, text="Description:     ")
                descriptionEntry = ttk.Entry(descriptionFrame, width=40)
                winversFrame = ttk.Frame(subframe)                
                winversText = ttk.Label(winversFrame, text="Windows versions: ")
                winverscheckvar1 = tk.IntVar()
                winverscheckvar1.set(0)
                winverscheck1 = ttk.Checkbutton(winversFrame, text="11", variable=winverscheckvar1)
                winverscheckvar2 = tk.IntVar()
                winverscheckvar2.set(0)
                winverscheck2 = ttk.Checkbutton(winversFrame, text="10", variable=winverscheckvar2)
                winverscheckvar3 = tk.IntVar()
                winverscheckvar3.set(0)
                winverscheck3 = ttk.Checkbutton(winversFrame, text="8.1", variable=winverscheckvar3)
                winverscheckvar4 = tk.IntVar()
                winverscheckvar4.set(0)
                winverscheck4 = ttk.Checkbutton(winversFrame, text="8", variable=winverscheckvar4)
                winverscheckvar5 = tk.IntVar()
                winverscheckvar5.set(0)
                winverscheck5 = ttk.Checkbutton(winversFrame, text="7", variable=winverscheckvar5)
                keyFrame = ttk.Frame(subframe)
                keyText = ttk.Label(keyFrame, text="Key:                  ")
                keyEntry = ttk.Entry(keyFrame, width=40)
                valueFrame = ttk.Frame(subframe)
                valueText = ttk.Label(valueFrame, text="Value:               ")
                valueEntry = ttk.Entry(valueFrame, width=40)
                typeFrame = ttk.Frame(subframe)
                typeText = ttk.Label(typeFrame, text="Type:                ")
                typeEntry = ttk.Entry(typeFrame, width=40)
                dataValuesFrame = ttk.Frame(subframe)
                dataValuesText = ttk.Label(dataValuesFrame, text="Data Values: ")
                enabledFrame = ttk.Frame(subframe)
                enabledText = ttk.Label(enabledFrame, text="Enabled:          ")
                enabledEntry = ttk.Entry(enabledFrame, width=2)
                disabledFrame = ttk.Frame(subframe)
                disabledText = ttk.Label(disabledFrame, text="Disabled:         ")
                disabledEntry = ttk.Entry(disabledFrame, width=2)
                displaynameText.pack(side="left", padx=(5,0))
                displaynameEntry.pack(side="left", padx=(5,0))
                descriptionText.pack(side="left", padx=(5,0))
                descriptionEntry.pack(side="left", padx=(5,0))
                winversText.pack(side="left", padx=5)
                winverscheck1.pack(side="left", padx=5)
                winverscheck2.pack(side="left", padx=5)
                winverscheck3.pack(side="left", padx=5)
                winverscheck4.pack(side="left", padx=5)
                winverscheck5.pack(side="left", padx=5)
                keyText.pack(side="left", padx=(5,0))
                keyEntry.pack(side="left", padx=(5,0))
                valueText.pack(side="left", padx=(5,0))
                valueEntry.pack(side="left", padx=(5,0))
                typeText.pack(side="left", padx=(5,0))
                typeEntry.pack(side="left", padx=(5,0))
                dataValuesText.pack(side="left", padx=(5,0))
                enabledText.pack(side="left", padx=(5,0))
                enabledEntry.pack(side="left", padx=(5,0))
                disabledText.pack(side="left", padx=(5,0))
                disabledEntry.pack(side="left", padx=(5,0))
                displaynameFrame.pack(anchor="w")
                descriptionFrame.pack(anchor="w")
                winversFrame.pack(anchor="w")
                keyFrame.pack(anchor="w")
                valueFrame.pack(anchor="w")
                typeFrame.pack(anchor="w")
                dataValuesFrame.pack(anchor="w")
                enabledFrame.pack(anchor="w")
                disabledFrame.pack(anchor="w")
                obj = {"dataType": dataType,
                    "subframe": subframe,
                    "radioSetFrame": radioSetFrame, 
                    "entryIndexText": entryIndexText,
                    "radioSet": rSet, 
                    "displaynameFrame": displaynameFrame,
                    "displaynameText": displaynameText, 
                    "displaynameEntry": displaynameEntry, 
                    "descriptionFrame": descriptionFrame,
                    "descriptionText": descriptionText, 
                    "descriptionEntry": descriptionEntry, 
                    "winversFrame": winversFrame,
                    "winversText": winversText,
                    "winverscheckvar1": winverscheckvar1, 
                    "winverscheck1": winverscheck1, 
                    "winverscheckvar2": winverscheckvar2, 
                    "winverscheck2": winverscheck2, 
                    "winverscheckvar3": winverscheckvar3, 
                    "winverscheck3": winverscheck3,
                    "winverscheckvar4": winverscheckvar4,
                    "winverscheck4": winverscheck4,
                    "winverscheckvar5": winverscheckvar5,
                    "winverscheck5": winverscheck5,
                    "keyFrame": keyFrame,
                    "keyText": keyText,
                    "keyEntry": keyEntry,
                    "valueFrame": valueFrame,
                    "valueText": valueText,
                    "valueEntry": valueEntry,
                    "typeFrame": typeFrame,
                    "typeText": typeText,
                    "typeEntry": typeEntry,
                    "dataValuesFrame": dataValuesFrame,
                    "dataValuesText": dataValuesText,
                    "enabledFrame": enabledFrame,
                    "enabledText": enabledText,
                    "enabledEntry": enabledEntry,
                    "disabledFrame": disabledFrame,
                    "disabledText": disabledText,
                    "disabledEntry": disabledEntry}
                for i in obj:
                    widget = obj[i]
                    NoneType = type(None)
                    if type(widget) is str or type(widget) is tk.IntVar or type(widget) is dict or type(widget) is NoneType:
                        pass
                    else:
                        widget.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
                if len(self.entriesList) >= 3:
                    self.canvasLength += 200
                    self.canvas.configure(scrollregion=(0,0,420,self.canvasLength))
            elif dataType == "Multi Value":
                def addValue():
                    valueCount = self.valueCountList[int(entryIndex)]
                    valueFrame = ttk.Frame(subframe)
                    nameEntry = ttk.Entry(valueFrame, width=25)
                    literallyJustAColon = ttk.Label(valueFrame, text=":")
                    dataEntry = ttk.Entry(valueFrame, width=10)
                    nameEntry.pack(side="left")
                    literallyJustAColon.pack(side="left")
                    dataEntry.pack(side="left")
                    valueFrame.pack()
                    valuesList = self.entriesList[f"{entryIndex}"]["values"]
                    valuesList["valueFrame" + str(valueCount)] = valueFrame
                    valuesList["nameEntry" + str(valueCount)] = nameEntry
                    valuesList["colon" + str(valueCount)] = literallyJustAColon
                    valuesList["dataEntry" + str(valueCount)] = dataEntry
                    self.entriesList[f'{entryIndex}']['values'] = valuesList
                    valueCount += 1
                    self.valueCountList[entryIndex] = valueCount
                    if len(self.entriesList) >= 3:
                        self.canvasLength += 25
                        self.canvas.configure(scrollregion=(0,0,420,self.canvasLength))
                displaynameFrame = ttk.Frame(subframe)
                displaynameText = ttk.Label(displaynameFrame, text="Display name: ")
                displaynameEntry = ttk.Entry(displaynameFrame, width=40)
                descriptionFrame = ttk.Frame(subframe)
                descriptionText = ttk.Label(descriptionFrame, text="Description:     ")
                descriptionEntry = ttk.Entry(descriptionFrame, width=40)
                winversFrame = ttk.Frame(subframe)                
                winversText = ttk.Label(winversFrame, text="Windows versions: ")
                winverscheckvar1 = tk.IntVar()
                winverscheckvar1.set(0)
                winverscheck1 = ttk.Checkbutton(winversFrame, text="11", variable=winverscheckvar1)
                winverscheckvar2 = tk.IntVar()
                winverscheckvar2.set(0)
                winverscheck2 = ttk.Checkbutton(winversFrame, text="10", variable=winverscheckvar2)
                winverscheckvar3 = tk.IntVar()
                winverscheckvar3.set(0)
                winverscheck3 = ttk.Checkbutton(winversFrame, text="8.1", variable=winverscheckvar3)
                winverscheckvar4 = tk.IntVar()
                winverscheckvar4.set(0)
                winverscheck4 = ttk.Checkbutton(winversFrame, text="8", variable=winverscheckvar4)
                winverscheckvar5 = tk.IntVar()
                winverscheckvar5.set(0)
                winverscheck5 = ttk.Checkbutton(winversFrame, text="7", variable=winverscheckvar5)
                keyFrame = ttk.Frame(subframe)
                keyText = ttk.Label(keyFrame, text="Key:                  ")
                keyEntry = ttk.Entry(keyFrame, width=40)
                valueFrame = ttk.Frame(subframe)
                valueText = ttk.Label(valueFrame, text="Value:               ")
                valueEntry = ttk.Entry(valueFrame, width=40)
                typeFrame = ttk.Frame(subframe)
                typeText = ttk.Label(typeFrame, text="Type:                ")
                typeEntry = ttk.Entry(typeFrame, width=40)
                dataValuesFrame = ttk.Frame(subframe)
                dataValuesText = ttk.Label(dataValuesFrame, text="Data Values: ")
                addValueBtn = ttk.Button(dataValuesFrame, text="+", width=2, command=lambda: addValue())
                displaynameText.pack(side="left", padx=(5,0))
                displaynameEntry.pack(side="left", padx=(5,0))
                descriptionText.pack(side="left", padx=(5,0))
                descriptionEntry.pack(side="left", padx=(5,0))
                winversText.pack(side="left", padx=5)
                winverscheck1.pack(side="left", padx=5)
                winverscheck2.pack(side="left", padx=5)
                winverscheck3.pack(side="left", padx=5)
                winverscheck4.pack(side="left", padx=5)
                winverscheck5.pack(side="left", padx=5)
                keyText.pack(side="left", padx=(5,0))
                keyEntry.pack(side="left", padx=(5,0))
                valueText.pack(side="left", padx=(5,0))
                valueEntry.pack(side="left", padx=(5,0))
                typeText.pack(side="left", padx=(5,0))
                typeEntry.pack(side="left", padx=(5,0))
                dataValuesText.pack(side="left", padx=(5,0))
                addValueBtn.pack(anchor="w", padx=13)
                displaynameFrame.pack(anchor="w")
                descriptionFrame.pack(anchor="w")
                winversFrame.pack(anchor="w")
                keyFrame.pack(anchor="w")
                valueFrame.pack(anchor="w")
                typeFrame.pack(anchor="w")
                dataValuesFrame.pack(anchor="w")
                obj = {"dataType": dataType,
                    "subframe": subframe,
                    "radioSetFrame": radioSetFrame, 
                    "entryIndexText": entryIndexText,
                    "radioSet": rSet, 
                    "displaynameFrame": displaynameFrame,
                    "displaynameText": displaynameText, 
                    "displaynameEntry": displaynameEntry, 
                    "descriptionFrame": descriptionFrame,
                    "descriptionText": descriptionText, 
                    "descriptionEntry": descriptionEntry, 
                    "winversFrame": winversFrame,
                    "winversText": winversText,
                    "winverscheckvar1": winverscheckvar1, 
                    "winverscheck1": winverscheck1, 
                    "winverscheckvar2": winverscheckvar2, 
                    "winverscheck2": winverscheck2, 
                    "winverscheckvar3": winverscheckvar3, 
                    "winverscheck3": winverscheck3,
                    "winverscheckvar4": winverscheckvar4,
                    "winverscheck4": winverscheck4,
                    "winverscheckvar5": winverscheckvar5,
                    "winverscheck5": winverscheck5,
                    "keyFrame": keyFrame,
                    "keyText": keyText,
                    "keyEntry": keyEntry,
                    "valueFrame": valueFrame,
                    "valueText": valueText,
                    "valueEntry": valueEntry,
                    "typeFrame": typeFrame,
                    "typeText": typeText,
                    "typeEntry": typeEntry,
                    "dataValuesFrame": dataValuesFrame,
                    "dataValuesText": dataValuesText,
                    "values": {}}
                for i in obj:
                    widget = obj[i]
                    NoneType = type(None)
                    if type(widget) is str or type(widget) is tk.IntVar or type(widget) is dict or type(widget) is NoneType:
                        pass
                    else:
                        widget.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
                if len(self.entriesList) >= 3:
                    self.canvasLength += 200
                    self.canvas.configure(scrollregion=(0,0,420,self.canvasLength))
            elif dataType == "Key":
                displaynameFrame = ttk.Frame(subframe)
                displaynameText = ttk.Label(displaynameFrame, text="Display name: ")
                displaynameEntry = ttk.Entry(displaynameFrame, width=40)
                descriptionFrame = ttk.Frame(subframe)
                descriptionText = ttk.Label(descriptionFrame, text="Description:     ")
                descriptionEntry = ttk.Entry(descriptionFrame, width=40)
                winversFrame = ttk.Frame(subframe)                
                winversText = ttk.Label(winversFrame, text="Windows versions: ")
                winverscheckvar1 = tk.IntVar()
                winverscheckvar1.set(0)
                winverscheck1 = ttk.Checkbutton(winversFrame, text="11", variable=winverscheckvar1)
                winverscheckvar2 = tk.IntVar()
                winverscheckvar2.set(0)
                winverscheck2 = ttk.Checkbutton(winversFrame, text="10", variable=winverscheckvar2)
                winverscheckvar3 = tk.IntVar()
                winverscheckvar3.set(0)
                winverscheck3 = ttk.Checkbutton(winversFrame, text="8.1", variable=winverscheckvar3)
                winverscheckvar4 = tk.IntVar()
                winverscheckvar4.set(0)
                winverscheck4 = ttk.Checkbutton(winversFrame, text="8", variable=winverscheckvar4)
                winverscheckvar5 = tk.IntVar()
                winverscheckvar5.set(0)
                winverscheck5 = ttk.Checkbutton(winversFrame, text="7", variable=winverscheckvar5)
                keyFrame = ttk.Frame(subframe)
                keyText = ttk.Label(keyFrame, text="Key:                  ")
                keyEntry = ttk.Entry(keyFrame, width=40)
                whatValueFrame = ttk.Frame(subframe)
                whatValueText = ttk.Label(whatValueFrame, text="Adding the key: ")
                whatValueVar = tk.IntVar()
                whatValueR1 = ttk.Radiobutton(whatValueFrame, variable=whatValueVar, text="Enables", value=1)
                whatValueR2 = ttk.Radiobutton(whatValueFrame, variable=whatValueVar, text="Disables", value=0)
                displaynameText.pack(side="left", padx=(5,0))
                displaynameEntry.pack(side="left", padx=(5,0))
                descriptionText.pack(side="left", padx=(5,0))
                descriptionEntry.pack(side="left", padx=(5,0))
                winversText.pack(side="left", padx=5)
                winverscheck1.pack(side="left", padx=5)
                winverscheck2.pack(side="left", padx=5)
                winverscheck3.pack(side="left", padx=5)
                winverscheck4.pack(side="left", padx=5)
                winverscheck5.pack(side="left", padx=5)
                keyText.pack(side="left", padx=(5,0))
                keyEntry.pack(side="left", padx=(5,0))
                whatValueText.pack(side="left", padx=5)
                whatValueR1.pack(side="left", padx=20)
                whatValueR2.pack(side="left")
                displaynameFrame.pack(anchor="w")
                descriptionFrame.pack(anchor="w")
                winversFrame.pack(anchor="w")
                keyFrame.pack(anchor="w")
                whatValueFrame.pack(anchor="w")
                obj = {"dataType": dataType,
                    "subframe": subframe,
                    "radioSetFrame": radioSetFrame, 
                    "entryIndexText": entryIndexText,
                    "radioSet": rSet, 
                    "displaynameFrame": displaynameFrame,
                    "displaynameText": displaynameText, 
                    "displaynameEntry": displaynameEntry, 
                    "descriptionFrame": descriptionFrame,
                    "descriptionText": descriptionText, 
                    "descriptionEntry": descriptionEntry, 
                    "winversFrame": winversFrame,
                    "winversText": winversText,
                    "winverscheckvar1": winverscheckvar1, 
                    "winverscheck1": winverscheck1, 
                    "winverscheckvar2": winverscheckvar2, 
                    "winverscheck2": winverscheck2, 
                    "winverscheckvar3": winverscheckvar3, 
                    "winverscheck3": winverscheck3,
                    "winverscheckvar4": winverscheckvar4,
                    "winverscheck4": winverscheck4,
                    "winverscheckvar5": winverscheckvar5,
                    "winverscheck5": winverscheck5,
                    "keyFrame": keyFrame,
                    "keyText": keyText,
                    "keyEntry": keyEntry,
                    "whatValueFrame": whatValueFrame,
                    "whatValueText": whatValueText,
                    "whatValueVar": whatValueVar,
                    "whatValueR1": whatValueR1,
                    "whatValueR2": whatValueR2}
                for i in obj:
                    widget = obj[i]
                    NoneType = type(None)
                    if type(widget) is str or type(widget) is tk.IntVar or type(widget) is dict or type(widget) is NoneType:
                        pass
                    else:
                        widget.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
                if len(self.entriesList) >= 3:
                    self.canvasLength += 200
                    self.canvas.configure(scrollregion=(0,0,420,self.canvasLength))
            elif dataType == "String":
                displaynameFrame = ttk.Frame(subframe)
                displaynameText = ttk.Label(displaynameFrame, text="Display name: ")
                displaynameEntry = ttk.Entry(displaynameFrame, width=40)
                descriptionFrame = ttk.Frame(subframe)
                descriptionText = ttk.Label(descriptionFrame, text="Description:     ")
                descriptionEntry = ttk.Entry(descriptionFrame, width=40)
                winversFrame = ttk.Frame(subframe)                
                winversText = ttk.Label(winversFrame, text="Windows versions: ")
                winverscheckvar1 = tk.IntVar()
                winverscheckvar1.set(0)
                winverscheck1 = ttk.Checkbutton(winversFrame, text="11", variable=winverscheckvar1)
                winverscheckvar2 = tk.IntVar()
                winverscheckvar2.set(0)
                winverscheck2 = ttk.Checkbutton(winversFrame, text="10", variable=winverscheckvar2)
                winverscheckvar3 = tk.IntVar()
                winverscheckvar3.set(0)
                winverscheck3 = ttk.Checkbutton(winversFrame, text="8.1", variable=winverscheckvar3)
                winverscheckvar4 = tk.IntVar()
                winverscheckvar4.set(0)
                winverscheck4 = ttk.Checkbutton(winversFrame, text="8", variable=winverscheckvar4)
                winverscheckvar5 = tk.IntVar()
                winverscheckvar5.set(0)
                winverscheck5 = ttk.Checkbutton(winversFrame, text="7", variable=winverscheckvar5)
                keyFrame = ttk.Frame(subframe)
                keyText = ttk.Label(keyFrame, text="Key:                  ")
                keyEntry = ttk.Entry(keyFrame, width=40)
                valueFrame = ttk.Frame(subframe)
                valueText = ttk.Label(valueFrame, text="Value:               ")
                valueEntry = ttk.Entry(valueFrame, width=40)
                typeFrame = ttk.Frame(subframe)
                typeText = ttk.Label(typeFrame, text="Type:                ")
                typeEntry = ttk.Entry(typeFrame, width=40)
                dataFrame = ttk.Frame(subframe)
                dataText = ttk.Label(dataFrame, text="Default Value: ")
                dataEntry = ttk.Entry(dataFrame, width=40)
                displaynameText.pack(side="left", padx=(5,0))
                displaynameEntry.pack(side="left", padx=(5,0))
                descriptionText.pack(side="left", padx=(5,0))
                descriptionEntry.pack(side="left", padx=(5,0))
                winversText.pack(side="left", padx=5)
                winverscheck1.pack(side="left", padx=5)
                winverscheck2.pack(side="left", padx=5)
                winverscheck3.pack(side="left", padx=5)
                winverscheck4.pack(side="left", padx=5)
                winverscheck5.pack(side="left", padx=5)
                keyText.pack(side="left", padx=(5,0))
                keyEntry.pack(side="left", padx=(5,0))
                valueText.pack(side="left", padx=(5,0))
                valueEntry.pack(side="left", padx=(5,0))
                typeText.pack(side="left", padx=(5,0))
                typeEntry.pack(side="left", padx=(5,0))
                dataText.pack(side="left", padx=(5,0))
                dataEntry.pack(side="left", padx=(5,0))
                displaynameFrame.pack(anchor="w")
                descriptionFrame.pack(anchor="w")
                winversFrame.pack(anchor="w")
                keyFrame.pack(anchor="w")
                valueFrame.pack(anchor="w")
                typeFrame.pack(anchor="w")
                dataFrame.pack(anchor="w")
                obj = {"dataType": dataType,
                    "subframe": subframe,
                    "radioSetFrame": radioSetFrame, 
                    "entryIndexText": entryIndexText,
                    "radioSet": rSet, 
                    "displaynameFrame": displaynameFrame,
                    "displaynameText": displaynameText, 
                    "displaynameEntry": displaynameEntry, 
                    "descriptionFrame": descriptionFrame,
                    "descriptionText": descriptionText, 
                    "descriptionEntry": descriptionEntry, 
                    "winversFrame": winversFrame,
                    "winversText": winversText,
                    "winverscheckvar1": winverscheckvar1, 
                    "winverscheck1": winverscheck1, 
                    "winverscheckvar2": winverscheckvar2, 
                    "winverscheck2": winverscheck2, 
                    "winverscheckvar3": winverscheckvar3, 
                    "winverscheck3": winverscheck3,
                    "winverscheckvar4": winverscheckvar4,
                    "winverscheck4": winverscheck4,
                    "winverscheckvar5": winverscheckvar5,
                    "winverscheck5": winverscheck5,
                    "keyFrame": keyFrame,
                    "keyText": keyText,
                    "keyEntry": keyEntry,
                    "valueFrame": valueFrame,
                    "valueText": valueText,
                    "valueEntry": valueEntry,
                    "typeFrame": typeFrame,
                    "typeText": typeText,
                    "typeEntry": typeEntry,
                    "dataFrame": dataFrame,
                    "dataText": dataText,
                    "dataEntry": dataEntry}
                for i in obj:
                    widget = obj[i]
                    NoneType = type(None)
                    if type(widget) is str or type(widget) is tk.IntVar or type(widget) is dict or type(widget) is NoneType:
                        pass
                    else:
                        widget.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
                if len(self.entriesList) >= 3:
                    self.canvasLength += 200
                    self.canvas.configure(scrollregion=(0,0,420,self.canvasLength))
            self.valueCountList.append(0)
            self.entriesList[f"{entryIndex}"] = obj
            addBtn.pack(padx=200, pady=15, anchor="s")

        entryIndex = self.entryCount
        radioVar = tk.StringVar()
        radioSet=None
        subframe = ttk.Frame(self.frame)
        subframe.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
        radioSetFrame = ttk.Frame(subframe)
        entryIndexText = ttk.Label(radioSetFrame, text=f"{int(self.entryCount) + 1}: ")
        if not self.entriesList:
            entryIndexText.pack(side="left", anchor="w", pady=10)
        elif self.entriesList:
            entryIndexText.pack(side="left", anchor="w", pady=(28,10))
        for dataType in dataTypes:
            radioSet = ttk.Radiobutton(radioSetFrame, text=dataType, value=dataType, variable=radioVar, command=lambda dataType=dataType, entryIndex=entryIndex, subframe=subframe, radioSet=radioSet: addEntryFull(self,dataType,entryIndex,subframe,radioSet, addBtn, entryIndexText))
            if not self.entriesList:
                radioSet.pack(side="left", anchor="w", pady=10)
            elif self.entriesList:
                radioSet.pack(side="left", anchor="w", pady=(28,10))
        if len(self.entriesList) >= 3:
            self.canvasLength += 50
            self.canvas.configure(scrollregion=(0,0,420,self.canvasLength))
        radioSetFrame.pack(fill="x")
        subframe.pack()
        obj = {"radioSetFrame": radioSetFrame, "radioSet": radioSet}
        self.entriesList[f"{self.entryCount}"] = obj
        addBtn.pack(padx=200, pady=15, anchor="s")
        self.entryCount += 1
    
    def helpMenu(self):
        IW = tk.Toplevel()
        IW.title("JSON Creator Usage Examples")
        IW.geometry('630x350')
        IW.resizable(False, False)
        canvas = tk.Canvas(IW, width=630, height=350, scrollregion=(0,0,630,600), highlightthickness=0)
        canvas.bind('<MouseWheel>', lambda event: canvas.yview_scroll(int(event.delta / -60), "units"))
        canvas.pack(fill=tk.BOTH)
        scrollbar = ttk.Scrollbar(IW, orient="vertical",command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(relx=1,rely=0,relheight=1,anchor="ne")
        frame = tk.Frame(canvas)
        frame.bind('<MouseWheel>', lambda event: canvas.yview_scroll(int(event.delta / -60), "units"))
        canvas.create_window((0, 0), window=frame, anchor=tk.NW)

        frame1 = ttk.Frame(frame)
        frame1.bind('<MouseWheel>', lambda event: canvas.yview_scroll(int(event.delta / -60), "units"))
        exTxt = ttk.Label(frame1, text="""Example 1: Double Value
Display name: Bing search
Description: Use Bing in the Windows search bar
Windows versions: 11, 10
Key: HKEY_USERS\Default\SOFTWARE\Microsoft\Windows\CurrentVersion\Search
Value: BingSearchEnabled
Type: REG_DWORD
Data Values:
        Enabled: 1
        Disabled: 0
        
Example 2: Multi Value
Display name: Taskbar search box
Description: Select size of the taskbar search box
Windows versions: 10
Key: HKEY_USERS\Default\SOFTWARE\Microsoft\Windows\CurrentVersion\Search
Value: SearchboxTaskbarMode
Type: REG_DWORD
Data Values:
        Hidden: 0
        Search icon: 1
        Search box: 2

Example 3: Key
Display name: New context menu
Description: Enable or disable the new right click context menu in Windows 11
Windows versions: 11
Key: HKEY_USERS\Default\SOFTWARE\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32
Adding the key: Disables

Example 4: String
Display name: Search box text
Description: Change the text in the Windows search box
Windows versions: 10
Key: HKEY_USERS\Default\SOFTWARE\Microsoft\Windows\CurrentVersion\Search\Flighting\\1\SearchBoxText
Value: Value
Type: REG_SZ
Default Value: \"Type here to search\"""")
        exTxt.bind('<MouseWheel>', lambda event: canvas.yview_scroll(int(event.delta / -60), "units"))
        exTxt.pack(side="left", padx=15, pady=10)
        frame1.pack()
        
    
    def Use(self):
        jsonData = None
        self.exportJson(save=False)
        self.importJson(jsonData)


icon = pkg_resources.resource_filename(__name__, "icon.ico")