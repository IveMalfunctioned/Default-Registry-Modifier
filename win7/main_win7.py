import tkinter as tk
from tkinter.filedialog import *
from tkinter import ttk
from classes_win7 import Hive
from jsoncreator_win7 import jsonCreator
from datetime import datetime
import platform
import subprocess
import requests
import ctypes, os
import pkg_resources
import json
import webbrowser

ver = "3.0"
hasInternet = 1
data = None

try:
    r = requests.get("https://raw.githubusercontent.com/IveMalfunctioned/Default-Registry-Modifier/main/keys.json")
    data = json.loads(r.text)

    #with open("G:\Desktop\Default Registry Modifier\keys_test.json", 'r') as file:
    #    data=json.loads(file.read())

    hasInternet = 1
except:
    hasInternet = 0

getWinver = subprocess.run("reg query \"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\" /v \"CurrentBuild\"", shell=True, capture_output=True)
winver = ""
for i in str(getWinver.stdout):
    if i.isdigit():
        winver = winver + i
if int(winver) >= 22000:
    winver = "11"
else:
    winver = platform.release()


def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

if isAdmin():

    DefaultHive = Hive(path="%SystemDrive%\\Users\\Default\\NTUSER.DAT")

    class MainApp:
        def __init__(self, window, data):
            self.window = window
            self.data = data

            self.ImplList = []

            self.incompatible = False

            menubar = tk.Menu(window)
            window.config(menu=menubar)

            filemenu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="File", menu=filemenu)
            
            filemenu.add_command(label="Import JSON data", command=self.importJson)
            filemenu.add_command(label="Use online JSON data", command=self.useOnlineJson)
            filemenu.add_command(label="Create backup", command=self.backup)
            filemenu.add_command(label="Export console log", command=self.exportConsole)

            keymenu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Key", menu=keymenu)
            keymenu.add_command(label="Save changes", command=self.commitConfirm)
            keymenu.add_command(label="Restart PC", command=self.restartPC)
            keymenu.add_command(label="Restart explorer", command=self.restartExplorer)

            infomenu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Info", menu=infomenu)
            infomenu.add_command(label="Open online JSON data", command=lambda: webbrowser.open_new("https://raw.githubusercontent.com/IveMalfunctioned/Default-Registry-Modifier/main/keys.json"))
            infomenu.add_command(label="Check for update", command=lambda: self.updateCheck(onStart=False))
            infomenu.add_command(label="About app", command=self.infoBox)

            jcmenu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="JSON Creator", menu=jcmenu)
            jcmenu.add_command(label="JSON Creator", command=self.jsonCreator)
            
            self.btns = []
            max1 = []
            descLength = 0
            if hasInternet:
                for i in self.data:
                    max1.append(self.data[str(i)]["description"])
                if len(max(max1, key=len)) >= 60:
                    descLength = (len(max(max1, key=len)) - 60) * 5
                self.canvas = tk.Canvas(window,scrollregion=(0,0,420+descLength,478+len(self.data)*80), highlightthickness=0)
            else:
                self.canvas = tk.Canvas(window, highlightthickness=0)
            self.canvas.config(width=420, height=476)
            self.canvas.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
            self.canvas.bind('<Shift-MouseWheel>', lambda event: self.canvas.xview_scroll(int(event.delta / -60), "units"))
            
            self.sbar = ttk.Scrollbar(window, orient="vertical", command=self.canvas.yview)
            self.canvas.config(yscrollcommand=self.sbar.set)
            self.sbar.place(relx=1,rely=0,relheight=.6,anchor="ne")

            self.sbarh = ttk.Scrollbar(window, orient="horizontal", command=self.canvas.xview)
            self.canvas.config(xscrollcommand=self.sbarh.set)
            self.sbarh.place(x=0,y=460, width=403)

            self.frame = tk.Frame(self.canvas)
            self.canvas.create_window((0, 0), window=self.frame, anchor=tk.NW)
            self.console = tk.Text(
                window,
                height = '20',
                width = window.winfo_reqwidth()
            )
            self.console.tag_configure("warning", foreground="red")
            self.console.insert("end", "Default Registry Modifier version " + ver + " - Console log\n\n")
            self.console.config(state="disabled")
            if hasInternet:
                self.updateCheck(onStart=True)
                self.addKeyEntries()
            else:
                self.NoConnect = tk.Label(self.canvas, text="Couldn't download online JSON data.\nImport offline JSON data by using\nFile > Import JSON data")
                self.NoConnect.pack(pady=25)
                self.console.config(state="normal")
                self.console.insert("end", "Couldn't download online JSON data\n", 'warning')
                self.console.config(state="disabled")
            self.canvas.pack(fill="both")
            self.console.pack(side="bottom")

            HStyle = ttk.Style()
            HStyle.configure("HStyle.TButton", background="#0000FF")
            NStyle = ttk.Style()
            NStyle.configure("NStyle.TButton", background="gray")
        
        def addKeyEntries(self):
            self.count = 1
            
            for i in self.data:
                self.inframe = tk.Frame(self.frame)
                self.inframe.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
                self.inframe.bind('<Shift-MouseWheel>', lambda event: self.canvas.xview_scroll(int(event.delta / -60), "units"))
                self.inframe.pack(fill="x")

                try:
                    txt = ttk.Label(self.inframe, text=str(self.count) + ": " + self.data[str(i)]['displayname'] + "\nDescription: " + self.data[str(i)]['description'] + f"\nWindows {', '.join(self.data[str(i)]['winversions'])}", anchor="w")
                    if winver in self.data[str(i)]['winversions']:
                        compattxt = ttk.Label(self.inframe, text="Compatible", foreground="green")
                    else:
                        compattxt = ttk.Label(self.inframe, text="Incompatible", foreground="red")
                except:
                    txt = ttk.Label(self.inframe, text=str(self.count) + ": " + self.data[str(i)]['displayname'] + "\nDescription: " + self.data[str(i)]['description'] + f"\nUnknown Windows version", anchor="w")
                    compattxt = ttk.Label(self.inframe, text="Cannot determine compatibility", foreground="#00004A")
                txt.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
                txt.bind('<Shift-MouseWheel>', lambda event: self.canvas.xview_scroll(int(event.delta / -60), "units"))
                txt.pack(anchor="w", padx=10, pady=(10,0))
                compattxt.pack(anchor="w", padx=10, pady=(0,5))

                if self.data[str(i)]["dataType"] == "OnOrOffV":
                    btnE = ttk.Button(self.inframe, text="Enable", style="NStyle.TButton", command=lambda i=i: self.addListing(i, self.data[str(i)]["dataType"], "enabled"))
                    btnE.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
                    btnE.bind('<Shift-MouseWheel>', lambda event: self.canvas.xview_scroll(int(event.delta / -60), "units"))
                    btnE.pack(side="left", padx=(20, 3))

                    btnD = ttk.Button(self.inframe, text="Disable", style="NStyle.TButton", command=lambda i=i: self.addListing(i, self.data[str(i)]["dataType"], "disabled"))
                    btnD.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
                    btnD.bind('<Shift-MouseWheel>', lambda event: self.canvas.xview_scroll(int(event.delta / -60), "units"))
                    btnD.pack(side="left")

                    btnP = ttk.Button(self.inframe, text="Properties", style="NStyle.TButton", command=lambda i=i: self.properties(i))
                    btnP.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
                    btnP.bind('<Shift-MouseWheel>', lambda event: self.canvas.xview_scroll(int(event.delta / -60), "units"))
                    btnP.pack(side="left", padx=3)

                    self.btns.append({"btnE" + str(i): btnE, "btnD" + str(i): btnD, "btnP" + str(i): btnP, "txt" + str(i): txt})
                elif self.data[str(i)]["dataType"] == "OnOrOffK":
                    btnE = ttk.Button(self.inframe, text="Enable", style="NStyle.TButton", command=lambda i=i: self.addListing(i, self.data[str(i)]["dataType"], "enabled"))
                    btnE.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
                    btnE.bind('<Shift-MouseWheel>', lambda event: self.canvas.xview_scroll(int(event.delta / -60), "units"))
                    btnE.pack(side="left", padx=(20, 3))

                    btnD = ttk.Button(self.inframe, text="Disable", style="NStyle.TButton", command=lambda i=i: self.addListing(i, self.data[str(i)]["dataType"], "disabled"))
                    btnD.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
                    btnD.bind('<Shift-MouseWheel>', lambda event: self.canvas.xview_scroll(int(event.delta / -60), "units"))
                    btnD.pack(side="left")

                    btnP = ttk.Button(self.inframe, text="Properties", style="NStyle.TButton", command=lambda i=i: self.properties(i))
                    btnP.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
                    btnP.bind('<Shift-MouseWheel>', lambda event: self.canvas.xview_scroll(int(event.delta / -60), "units"))
                    btnP.pack(side="left", padx=3)

                    self.btns.append({"btnE" + str(i): btnE, "btnD" + str(i): btnD, "btnP" + str(i): btnP, "txt" + str(i): txt})
                elif self.data[str(i)]["dataType"] == "OnOrOffMV":
                    MVlist = []
                    a = 0
                    self.valuesCount = 0
                    for value in self.data[str(i)]["values"]:
                        btnV = ttk.Button(self.inframe, text=value, command=lambda i=i, val=value, iBtn=self.valuesCount: self.addListing(i, self.data[str(i)]["dataType"], value=val, iBtn=iBtn), style="NStyle.TButton")
                        btnV.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
                        btnV.bind('<Shift-MouseWheel>', lambda event: self.canvas.xview_scroll(int(event.delta / -60), "units"))
                        MVlist.append({"btnV" + str(self.valuesCount): btnV})
                        if not a:
                            btnV.pack(side="left", padx=(20,3))
                            a += 1
                        else:
                            btnV.pack(side="left", padx=(0,3))
                        self.valuesCount += 1
                            
                    btnP = ttk.Button(self.inframe, text="Properties", style="NStyle.TButton", command=lambda i=i: self.properties(i))
                    btnP.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
                    btnP.bind('<Shift-MouseWheel>', lambda event: self.canvas.xview_scroll(int(event.delta / -60), "units"))
                    btnP.pack(side="left")

                    self.btns.append({"mvBtns" + i: MVlist, "btnP" + i: btnP})
                elif self.data[str(i)]["dataType"] == "String":
                    self.entry_var = tk.StringVar()
                    self.entry_var.trace("w", lambda *args, i=i, dataType=self.data[str(i)]["dataType"]: passString(i, dataType))
                    strEntry = ttk.Entry(self.inframe, text="Hello", width=38, textvariable=self.entry_var)
                    strEntry.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
                    strEntry.bind('<Shift-MouseWheel>', lambda event: self.canvas.xview_scroll(int(event.delta / -60), "units"))

                    strEntry.pack(side="left", padx=(20,3))

                    btnP = ttk.Button(self.inframe, text="Properties", style="NStyle.TButton", command=lambda i=i: self.properties(i))
                    btnP.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
                    btnP.bind('<Shift-MouseWheel>', lambda event: self.canvas.xview_scroll(int(event.delta / -60), "units"))
                    btnP.pack(side="left")

                    self.btns.append({"strBox" + i: strEntry, "btnP" + i: btnP})
                else:
                    pass
                    
                self.count += 1
                def passString(i, dataType):
                    string = self.entry_var.get()
                    obj = {str(i): {"dataType": dataType}}
                    if string:
                        if obj not in self.ImplList:
                            self.ImplList.append(obj)
                    elif string == "":
                        self.ImplList.remove(obj)

        def addListing(self, i, dataType, value, iBtn=None):
            if dataType == "OnOrOffV" or dataType == "OnOrOffK":
                obj = {str(i): {"dataType": dataType, "value": value}}
                if value == "enabled":
                    opposite_value = "disabled"
                    btn = self.btns[int(i)]['btnE' + str(i)]
                    opposite_btn = self.btns[int(i)]['btnD' + str(i)]
                elif value == "disabled":
                    opposite_value = "enabled"
                    btn = self.btns[int(i)]['btnD' + str(i)]
                    opposite_btn = self.btns[int(i)]['btnE' + str(i)]
                oppositeObj = {str(i): {"dataType": dataType, "value": opposite_value}}
                if oppositeObj in self.ImplList:
                    self.ImplList.remove(oppositeObj)
                    opposite_btn.config(style="NStyle.TButton")
                if obj not in self.ImplList:
                    self.ImplList.append(obj)
                    btn.config(style="HStyle.TButton")
                elif obj in self.ImplList:
                    self.ImplList.remove(obj)
                    btn.config(style="NStyle.TButton")
            elif dataType == "OnOrOffMV":
                entryBtns = self.btns[int(i)]['mvBtns' + str(i)]
                btnObj = entryBtns[iBtn]
                btn = btnObj["btnV" + str(iBtn)]
                obj = {str(i): {"dataType": dataType, "value": value}}
                for count, btnDict in enumerate(entryBtns):
                    if btnDict != btnObj:
                        otherBtn = btnDict["btnV" + str(count)]
                        otherBtn.config(style="NStyle.TButton")
                        otherObj = {str(i): {"dataType": dataType, "value": otherBtn.cget("text")}}
                        if otherObj in self.ImplList:
                            self.ImplList.remove(otherObj)
                if obj not in self.ImplList:
                    self.ImplList.append(obj)
                    btn.config(style="HStyle.TButton")
                elif obj in self.ImplList:
                    self.ImplList.remove(obj)
                    btn.config(style="NStyle.TButton")
            if winver not in self.data[str(i)]['winversions']:
                self.incompatible = True
    
        def properties(self, i):
            IW = tk.Toplevel()
            IW.title("Key Properties")
            if ((len(self.data[str(i)]['key']))+5)*6.5 > ((len(self.data[str(i)]['description']))+13)*5.45:
                L=str(int((int(len(self.data[str(i)]['key']))+5)*6.5))
                if int(L) < 340:
                    L = "340"
            else:
                L=str(int((int(len(self.data[str(i)]['description']))+13)*5.45))
                if int(L) < 340:
                    L = "340"
            IW.geometry(f'{L}x300')
            IW.resizable(False, False)
            values = ""
            hasStates = False
            if "values" in self.data[str(i)]:
                for state in self.data[str(i)]["values"]:
                    values = values + f"{state.capitalize()}: {self.data[str(i)]['values'][state]}\n"
                hasStates = True
            frame = tk.Frame(IW)
            infotext1 = ttk.Label(frame, text="Click here to copy all info", cursor="hand2")
            if hasStates:
                infotext1.bind("<Button-1>", lambda e: self.copy(txt=f"Display name: {self.data[str(i)]['displayname']}\nDescription: {self.data[str(i)]['description']}\nUsed in: Windows {', '.join(self.data[str(i)]['winversions'])}\nValue: {self.data[str(i)]['value']}\nKey: {self.data[str(i)]['key']}\nType: {self.data[str(i)]['type']}\nData Values:\n{values}"))
            else:
                infotext1.bind("<Button-1>", lambda e: self.copy(txt=f"Display name: {self.data[str(i)]['displayname']}\nDescription: {self.data[str(i)]['description']}\nUsed in: Windows {', '.join(self.data[str(i)]['winversions'])}\nValue: {self.data[str(i)]['value']}\nKey: {self.data[str(i)]['key']}\nType: {self.data[str(i)]['type']}\nDefault String: \"{self.data[str(i)]['DefaultValue']}\""))
            infotext1.pack(pady=(15,0))
            infotext2 = ttk.Label(frame, text="Click a particular detail to copy it")
            infotext2.pack(pady=(0,5))
            keytxt1 = ttk.Label(frame, text=f"Display name: {self.data[str(i)]['displayname']}", cursor="hand2")
            keytxt1.bind("<Button-1>", lambda e: self.copy(txt=f"{self.data[str(i)]['displayname']}"))
            keytxt1.pack(anchor="w")
            keytxt2 = ttk.Label(frame, text=f"Description: {self.data[str(i)]['description']}", cursor="hand2")
            keytxt2.bind("<Button-1>", lambda e: self.copy(txt=f"{self.data[str(i)]['description']}"))
            keytxt2.pack(anchor="w")
            keytxt3 = ttk.Label(frame, text=f"Used in: Windows {', '.join(self.data[str(i)]['winversions'])}", cursor="hand2")
            keytxt3.bind("<Button-1>", lambda e: self.copy(txt=f"Windows {', '.join(self.data[str(i)]['winversions'])}"))
            keytxt3.pack(anchor="w")
            try:
                keytxt4 = ttk.Label(frame, text=f"Value: {self.data[str(i)]['value']}", cursor="hand2")
                keytxt4.bind("<Button-1>", lambda e: self.copy(txt=f"{self.data[str(i)]['value']}"))
                keytxt4.pack(anchor="w")
            except:
                pass
            keytxt5 = ttk.Label(frame, text=f"Key: {self.data[str(i)]['key']}", cursor="hand2")
            keytxt5.bind("<Button-1>", lambda e: self.copy(txt=f"{self.data[str(i)]['key']}"))
            keytxt5.pack(anchor="w")
            if "type" in self.data[str(i)]:
                keytxt6 = ttk.Label(frame, text=f"Type: {self.data[str(i)]['type']}", cursor="hand2")
                keytxt6.bind("<Button-1>", lambda e: self.copy(txt=f"{self.data[str(i)]['type']}"))
                keytxt6.pack(anchor="w")
            
            if hasStates:
                keytxt7 = ttk.Label(frame, text="Data Values: ", cursor="hand2")
                keytxt7.bind("<Button-1>", lambda e: self.copy(txt=f"Values:\n{values}"))
                keytxt7.pack(anchor="w")
                keytxt8 = ttk.Label(frame, text=values, cursor="hand2")
                keytxt8.bind("<Button-1>", lambda e: self.copy(txt=f"Values:\n{values}"))
                keytxt8.pack(anchor="w", padx=25)
                cpady=0
            else:
                keytxt7 = ttk.Label(frame, text=f"Default String: \"{self.data[str(i)]['DefaultValue']}\"", cursor="hand2")
                keytxt7.bind("<Button-1>", lambda e: self.copy(txt=f"{self.data[str(i)]['DefaultValue']}"))
                keytxt7.pack(anchor="w")
                cpady=15
            
            closeBtn = ttk.Button(frame, text="Close", command=IW.destroy, style="NStyle.TButton")
            closeBtn.pack(pady=cpady, padx=25)
            frame.pack()

        def copy(self, txt):
            window.clipboard_clear()
            window.clipboard_append(txt)

        def commitConfirm(self):
            if not self.ImplList:
                self.console.config(state="normal")
                self.console.insert('end', "Must select values!\n\n")
                self.console.config(state="disabled")
            else:
                confirm = tk.Toplevel()
                confirm.title("Confirmation")
                confirm.geometry('420x200')
                confirm.resizable(False, False)
                infotxt = tk.Label(confirm, text="Apply tweaks to default user?\nIt is highly recommended that you create a backup first!")
                infotxt.pack(pady=(25,0))
                if self.incompatible:
                    incompatTxt = tk.Label(confirm, text="Incompatible tweaks selected, proceed with adding them to the registry?", foreground="red")
                    incompatTxt.pack()
                confirmFrame = tk.Frame(confirm)
                confirmFrame.pack()
                btnBk = ttk.Button(confirmFrame, text="Create backup", command=self.backup, style="NStyle.TButton", width=25)
                btnBk.pack(pady=8)
                btnY = ttk.Button(confirmFrame, text="Yes", command=lambda: self.commit(confirm), style="NStyle.TButton")
                btnY.pack(side="left", padx=(5, 4))
                btnN = ttk.Button(confirmFrame, text="No", command=confirm.destroy, style="NStyle.TButton")
                btnN.pack(side="left", padx=(4, 5))

        
        def commit(self, confirm):
            confirm.destroy()
            DefaultHive.load()
            if DefaultHive.outputStatus == 0:
                self.console.config(state="normal")
                self.console.insert('end', DefaultHive.output + "\n")
                self.console.config(state="disabled")
                for impl in self.ImplList:
                    i = next(iter(impl.keys()))
                    dataType = impl[i]['dataType']
                    if dataType != "String":
                        value = impl[i]['value']
                    else:
                        value = str("\"" + self.entry_var.get() + "\"")
                    # print(f"Index: {i}, dataType: {dataType}, Value: {value}")
                    key="\"" + self.data[str(i)]['key'] + "\""
                    if dataType == "OnOrOffV":
                        DefaultHive.add(key=key, value=self.data[str(i)]['value'], type=self.data[str(i)]['type'], data=self.data[str(i)]['values'][value], i=i, jsonData=self.data, dataType=dataType, valueName=value)
                        #print(DefaultHive.outputStatus)
                        if DefaultHive.outputStatus == 0:
                            self.console.config(state="normal")
                            self.console.insert('end', DefaultHive.output + "\n")
                            self.console.config(state="disabled")
                            self.btns[int(i)][str('btnE' + i)].config(style="NStyle.TButton")
                            self.btns[int(i)][str('btnD' + i)].config(style="NStyle.TButton")
                        elif DefaultHive.outputStatus == 1:
                            self.console.config(state="normal")
                            self.console.insert('end', DefaultHive.output + "\n", 'warning')
                            self.console.config(state="disabled")
                            self.btns[int(i)][str('btnE' + i)].config(style="NStyle.TButton")
                            self.btns[int(i)][str('btnD' + i)].config(style="NStyle.TButton")
                    elif dataType == "OnOrOffMV":
                        DefaultHive.add(key=key, value=self.data[str(i)]['value'], type=self.data[str(i)]['type'], data=self.data[str(i)]['values'][value], i=i, jsonData=self.data, dataType=dataType, valueName=value)
                        #print(DefaultHive.outputStatus)
                        if DefaultHive.outputStatus == 0:
                            self.console.config(state="normal")
                            self.console.insert('end', DefaultHive.output + "\n")
                            self.console.config(state="disabled")
                            entryBtns = self.btns[int(i)]['mvBtns' + str(i)]
                            for count, btnDict in enumerate(entryBtns):
                                Btn = btnDict["btnV" + str(count)]
                                Btn.config(style="NStyle.TButton")
                        elif DefaultHive.outputStatus == 1:
                            self.console.config(state="normal")
                            self.console.insert('end', DefaultHive.output + "\n", 'warning')
                            self.console.config(state="disabled")
                            for count, btnDict in enumerate(entryBtns):
                                Btn = btnDict["btnV" + str(count)]
                                Btn.config(style="NStyle.TButton")
                    elif dataType == "OnOrOffK":
                        DefaultHive.add(key=key, i=i, jsonData=self.data, dataType=dataType, valueName=value)
                        if "Deleted key" in DefaultHive.output:
                            DefaultHive.output = "Disabled key " + self.data[str(i)]['displayname']
                        else:
                            if DefaultHive.outputStatus == 0:
                                self.console.config(state="normal")
                                self.console.insert('end', DefaultHive.output + "\n")
                                self.console.config(state="disabled")
                                self.btns[int(i)][str('btnE' + i)].config(style="NStyle.TButton")
                                self.btns[int(i)][str('btnD' + i)].config(style="NStyle.TButton")
                            elif DefaultHive.outputStatus == 1:
                                self.console.config(state="normal")
                                self.console.insert('end', DefaultHive.output + "\n", 'warning')
                                self.console.config(state="disabled")
                                self.btns[int(i)][str('btnE' + i)].config(style="NStyle.TButton")
                                self.btns[int(i)][str('btnD' + i)].config(style="NStyle.TButton")
                    elif dataType == "String":
                        DefaultHive.add(key=key, value=self.data[str(i)]['value'], type=self.data[str(i)]['type'], data=value, i=i, jsonData=self.data, dataType=dataType)
                        #print(DefaultHive.output)
                        if DefaultHive.outputStatus == 0:
                            self.console.config(state="normal")
                            self.console.insert('end', DefaultHive.output + "\n")
                            self.console.config(state="disabled")
                            for widget in self.inframe.winfo_children():
                                if isinstance(widget, ttk.Entry):
                                    widget.delete(0, 'end')
                        elif DefaultHive.outputStatus == 1:
                            self.console.config(state="normal")
                            self.console.insert('end', DefaultHive.output + "\n", 'warning')
                            self.console.config(state="disabled")
                            for widget in self.inframe.winfo_children():
                                if isinstance(widget, ttk.Entry):
                                    widget.delete(0, 'end')
            DefaultHive.unload()
            if DefaultHive.outputStatus == 0:
                self.console.config(state="normal")
                self.console.insert('end', DefaultHive.output + "\n")
                self.console.insert('end', "Completed\n\n")
                self.console.config(state="disabled")
            else:
                self.console.config(state="normal")
                self.console.insert('end', DefaultHive.output + "\n", 'warning')
                self.console.insert('end', "Completed\n\n")
                self.console.config(state="disabled")
            self.ImplList = []
            self.incompatible = False
        
        def infoBox(self):
            IW = tk.Toplevel()
            IW.title("Application Info")
            IW.geometry('420x200')
            IW.resizable(False, False)
            label = tk.Label(IW, text=f"Default Registry Modifier version {ver}\nCreated by IveMalfunctioned\nPython version {platform.python_version()}\n{platform.system()} {winver} {platform.architecture()[0]}\nClick to copy", cursor="hand2")
            label.bind("<Button-1>", lambda e: self.copy(txt=f"Default Registry Modifier version {ver}\nPython version {platform.python_version()}\n{platform.system()} {winver} {platform.architecture()[0]}"))
            label.pack(pady=15)
            glink = tk.Label(IW, text="GitHub", fg="#0368BA", cursor="hand2")
            glink.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/IveMalfunctioned"))
            glink.pack()
            slink = tk.Label(IW, text="Source code", fg="#0368BA", cursor="hand2")
            slink.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/IveMalfunctioned/Default-Registry-Modifier"))
            slink.pack()
            dlink = tk.Label(IW, text="Discord", fg="#0368BA", cursor="hand2")
            dlink.bind("<Button-1>", lambda e: webbrowser.open_new("https://discord.gg/hzScjC9re6"))
            dlink.pack()
        
        def updateCheck(self, onStart):
            def throwError(self, onStart):
                if not onStart:
                    self.console.config(state="normal")
                    self.console.insert('end', "Couldn't check for update\n", 'warning')
                    self.console.config(state="disabled")
                else:
                    return
            try:
                response = requests.get("https://api.github.com/repos/IveMalfunctioned/Default-Registry-Modifier/releases/latest")
            except:
                throwError(self, onStart)
                return
            Fver = ""
            charCount = 0
            for char in str(response.json()["name"]):
                if charCount == 0:
                    charCount += 1
                elif charCount > 0:
                    if charCount >= 4:
                        break
                    elif charCount < 4:
                        Fver = Fver + char
                        charCount += 1
            if float(Fver) > float(ver):
                if not onStart:
                    IW = tk.Toplevel()
                    IW.geometry('200x240')
                    IW.resizable(False, False)
                    IW.title("Update found")
                    frame = tk.Frame(IW)
                    label = tk.Label(frame, text=f"Update found!\nLatest: {response.json()['name']}\nCurrent: " + ver)
                    dlBtn = ttk.Button(frame, text="Download", command=lambda: webbrowser.open_new("https://github.com/IveMalfunctioned/Default-Registry-Modifier/releases/latest"), style="NStyle.TButton")
                    noBtn = ttk.Button(frame, text="Cancel", command=IW.destroy, style="NStyle.TButton")
                    label.pack(pady=35)
                    frame.pack(fill="x")
                    dlBtn.pack(pady=5)
                    noBtn.pack()

                self.console.config(state="normal")
                self.console.insert('end', f"Application update found!\nLatest:  v{Fver}\nCurrent: v{ver}\n\n")
                self.console.config(state="disabled")
            elif float(ver) >= float(Fver):
                if not onStart:
                    IW = tk.Toplevel()
                    IW.geometry('200x240')
                    IW.resizable(False, False)
                    IW.title("Using latest version")
                    frame = tk.Frame(IW)
                    label = tk.Label(frame, text="You're using the\nlatest version: " + ver)
                    noBtn = ttk.Button(frame, text="Close", command=IW.destroy, style="NStyle.TButton")
                    label.pack(pady=40)
                    noBtn.pack()
                    frame.pack(fill="x")

        def restartExplorer(self):
            self.console.config(state="normal")
            self.console.insert('end', "Restarting explorer\n")
            self.console.config(state="disabled")
            subprocess.run("taskkill /f /im explorer.exe && explorer.exe", shell=True)

        def restartPC(self):
            def restart(text, btnY, btnN):
                def nvm():
                    subprocess.run("shutdown /a", shell=True)
                    IW.destroy()
                btnY.destroy()
                btnN.destroy()
                text.config(text="Restarting in 10 seconds")
                btnRN = ttk.Button(frame, text="Restart now", command=lambda: subprocess.run("shutdown /a && shutdown /r /t 0", shell=True), style="NStyle.TButton")
                btnC = ttk.Button(frame, text="Cancel restart", command=nvm, style="NStyle.TButton")
                btnRN.pack(pady=5, padx=(25, 5), side="left")
                btnC.pack(side="left")
                subprocess.run("shutdown /r /t 10")
            IW = tk.Toplevel()
            IW.geometry('420x200')
            IW.resizable(False, False)
            IW.title("Are you sure?")
            frame = tk.Frame(IW)
            text = ttk.Label(frame, text="Are you sure you want to restart your PC?\n     Make sure to save all your work first!")
            btnY = ttk.Button(frame, text="Yes", command=lambda: restart(text=text, btnY=btnY, btnN=btnN), style="NStyle.TButton")
            btnN = ttk.Button(frame, text="No", command=IW.destroy, style="NStyle.TButton")
            text.pack(pady=25)
            btnY.pack(pady=5, padx=(35, 5), side="left")
            btnN.pack(side="left")
            frame.pack()
        
        def importJson(self, jsonData=None):
            done=False
            if jsonData == None:
                newData = askopenfilename(defaultextension=".json")
                if newData:
                    newData = newData.replace("/", "\\")
                    try:
                        with open(newData, 'r') as file:
                            self.data = json.loads(file.read())
                            done=True
                    except:
                        self.console.config(state="normal")
                        self.console.insert('end', "Could not import JSON data: Formatting error\n", 'warning')
                        self.console.config(state="disabled")
                        return
            else:
                self.data = jsonData
                done=True
            if done == True:
                self.count = 1
                self.implList = []
                self.incompatible = False
                for i, value in enumerate(self.btns):
                    try:
                        value["btnE" + str(i)].destroy()
                        value["btnD" + str(i)].destroy()
                        value["btnP" + str(i)].destroy()
                        value["txt" + str(i)].destroy()
                    except:
                        pass
                    try:
                        entryBtns = self.btns[int(i)]['mvBtns' + str(i)]
                        for count, btnDict in enumerate(entryBtns):
                            Btn = btnDict["btnV" + str(count)]
                            Btn.destroy()
                    except:
                        pass
                for widget in self.frame.winfo_children():
                    widget.destroy()
                try:
                    self.NoConnect.destroy()
                except:
                    pass
                max1 = []
                for i in self.data:
                    max1.append(self.data[str(i)]["description"])
                if len(max(max1, key=len)) >= 60:
                    descLength = (len(max(max1, key=len)) - 60) * 5
                else:
                    descLength = 0
                self.canvas.configure(scrollregion=(0,0,420+descLength,478+len(self.data)*80))
                self.btns = []
                self.addKeyEntries()
                if not jsonData:
                    self.console.config(state="normal")
                    self.console.insert('end', "Imported JSON data from " + newData + "\n")
                    self.console.config(state="disabled")
        
        def useOnlineJson(self):
            try:
                r = requests.get("https://raw.githubusercontent.com/IveMalfunctioned/Default-Registry-Modifier/main/keys.json")
                try:
                    data = json.loads(r.text)
                except:
                    self.console.config(state="normal")
                    self.console.insert('end', "Data is not formatted properly. Please report this issue on GitHub (can be found in Info > About App\n", 'warning')
                    self.console.config(state="disabled")
                    return
            except:
                self.console.config(state="normal")
                self.console.insert('end', "Couldn't download online JSON data\n", 'warning')
                self.console.config(state="disabled")
                return
            self.importJson(jsonData=data)
            self.console.config(state="normal")
            self.console.insert('end', "Imported JSON data from GitHub\n")
            self.console.config(state="disabled")
            

        def backup(self):
            var = subprocess.check_output("powershell \"[Environment]::GetFolderPath('Desktop')\"", shell=True)
            path = asksaveasfilename(title="Save backup of default user hive", defaultextension=".DAT", initialdir=str(var.decode('utf-8')), initialfile="NTUSER.DAT", filetypes=[("DAT files", "*.DAT"), ("All Files", "*.*")])
            if path:
                path = path.replace("/", "\\")
                copy = subprocess.run(f"copy /v {DefaultHive.path} \"{path}\"", shell=True, capture_output=True, text=True)
                if "Access is denied" in copy.stdout:
                    self.console.config(state="normal")
                    self.console.insert('end', f"Could not copy {DefaultHive.path} to {path}. Access was denied\n", 'warning')
                    self.console.config(state="disabled")
                else:
                    self.console.config(state="normal")
                    self.console.insert('end', f"Created backup of {DefaultHive.path} at {path}\n")
                    self.console.config(state="disabled")
        
        def exportConsole(self):
            date=f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day} {datetime.now().hour}.{datetime.now().minute}.{datetime.now().second}"
            path = asksaveasfilename(defaultextension=".txt", initialfile="drm-log " + date, 
                              filetypes=[("Log files","*.log"), ("All Files","*.*")])
            if path:
                with open(path, 'w') as f:
                    txt = self.console.get(1.0, "end")
                    f.writelines(txt)
                    f.close()
                    self.console.config(state="normal")
                    self.console.insert('end', f"Exported console log to {path}\n")
                    self.console.config(state="disabled")
        
        def jsonCreator(self):
            IW = tk.Toplevel()
            IW.geometry('420x700')
            IW.resizable(False, False)
            IW.title("JSON Creator")
            main = jsonCreator(IW, self.importJson)


    icon = pkg_resources.resource_filename(__name__, "icon.ico")

    window = tk.Tk()
    window.geometry('420x800')
    window.resizable(False, False)
    window.title("Default Registry Modifier")
    window.iconbitmap(default=icon)
    main = MainApp(window, data)
    window.mainloop()

else:
    window = tk.Tk()
    window.geometry('350x100')
    window.resizable(False, False)
    window.title("Program needs admin privileges")
    icon = pkg_resources.resource_filename(__name__, "icon.ico")
    window.iconbitmap(default=icon)
    label = tk.Label(window, text="This program requires administrator privileges to run.\nPlease rerun the program as administrator and try again")
    label.pack()
    button = tk.Button(window, text="Exit", command=window.destroy)
    button.pack()
    window.mainloop()
