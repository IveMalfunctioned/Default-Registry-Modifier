import tkinter as tk
from tkinter.filedialog import *
from tkinter import ttk
from classes import Hive
from platform import python_version
import subprocess
import requests
import ctypes, os
import pkg_resources
import json
import webbrowser

ver = "2.0"
hasInternet = 1
data = None

try:
    r = requests.get("https://raw.githubusercontent.com/IveMalfunctioned/Default-Registry-Modifier/main/keys.json")
    data = json.loads(r.text)

    #with open("G:\Desktop\Default Registry Modifier\keys.json", 'r') as file:
    #   data=json.loads(file.read())
    
    hasInternet = 1
except:
    hasInternet = 0

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

            self.listE = []
            self.listD = []

            menubar = tk.Menu(window)
            window.config(menu=menubar)

            filemenu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="File", menu=filemenu)
            
            filemenu.add_command(label="Import JSON data", command=self.importJson)
            filemenu.add_command(label="Use online JSON data", command=self.useOnlineJson)
            filemenu.add_command(label="Create backup", command=self.backup)

            keymenu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Key", menu=keymenu)
            keymenu.add_command(label="Save changes", command=self.commitConfirm)

            infomenu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Info", menu=infomenu)
            infomenu.add_command(label="Open online JSON data", command=lambda: webbrowser.open_new("https://raw.githubusercontent.com/IveMalfunctioned/Default-Registry-Modifier/main/keys.json"))
            infomenu.add_command(label="About app", command=self.infoBox)
            
            self.btns = []
            max1 = []
            descLength = 0
            if hasInternet:
                for i in self.data:
                    max1.append(self.data[str(i)]["description"])
                if len(max(max1, key=len)) >= 60:
                    descLength = (len(max(max1, key=len)) - 60) * 5
                self.canvas = tk.Canvas(window,scrollregion=(0,0,420+descLength,478+len(self.data)*37), highlightthickness=0)
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

                txt = ttk.Label(self.inframe, text=str(self.count) + ": " + self.data[str(i)]['displayname'] + "\nDescription: " + self.data[str(i)]['description'], anchor="w")
                txt.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
                txt.bind('<Shift-MouseWheel>', lambda event: self.canvas.xview_scroll(int(event.delta / -60), "units"))
                txt.pack(anchor="w", padx=10, pady=(10,5))

                btnE = ttk.Button(self.inframe, text="Enable", style="NStyle.TButton", command=lambda i=i: self.enable(i))
                btnE.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
                btnE.bind('<Shift-MouseWheel>', lambda event: self.canvas.xview_scroll(int(event.delta / -60), "units"))
                btnE.pack(side="left", padx=(20, 3))

                btnD = ttk.Button(self.inframe, text="Disable", style="NStyle.TButton", command=lambda i=i: self.disable(i))
                btnD.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
                btnD.bind('<Shift-MouseWheel>', lambda event: self.canvas.xview_scroll(int(event.delta / -60), "units"))
                btnD.pack(side="left")

                btnR = ttk.Button(self.inframe, text="Remove", style="NStyle.TButton", command=lambda i=i: self.remove(i))
                btnR.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
                btnR.bind('<Shift-MouseWheel>', lambda event: self.canvas.xview_scroll(int(event.delta / -60), "units"))
                btnR.pack(side="left", padx=3)

                self.btns.append({"btnE" + str(i): btnE, "btnD" + str(i): btnD, "btnR" + str(i): btnR, "txt" + str(i): txt})
                self.count += 1
        
        def enable(self, i):
            if str(i) not in self.listE:
                self.listE.append(str(i))
            if str(i) in self.listD:
                self.listD.remove(str(i))
            self.btns[int(i)][str('btnE' + i)].config(style="HStyle.TButton")
            self.btns[int(i)][str('btnD' + i)].config(style="NStyle.TButton")

        def disable(self, i):
            if str(i) not in self.listD:
                self.listD.append(str(i))
            if str(i) in self.listE:
                self.listE.remove(str(i))
            self.btns[int(i)][str('btnE' + i)].config(style="NStyle.TButton")
            self.btns[int(i)][str('btnD' + i)].config(style="HStyle.TButton")
        
        def remove(self, i):
            if str(i) in self.listE:
                self.listE.remove(str(i))
            if str(i) in self.listD:
                self.listD.remove(str(i))
            self.btns[int(i)][str('btnE' + i)].config(style="NStyle.TButton")
            self.btns[int(i)][str('btnD' + i)].config(style="NStyle.TButton")
        
        def commitConfirm(self):
            if not self.listE and not self.listD:
                self.console.config(state="normal")
                self.console.insert('end', "Must select values!\n\n")
                self.console.config(state="disabled")
            else:
                confirm = tk.Toplevel()
                confirm.title("Confirmation")
                confirm.geometry('420x200')
                confirm.resizable(False, False)
                infotxt = tk.Label(confirm, text="Apply tweaks to default user?\nIt is highly recommended that you create a backup first!")
                infotxt.pack(pady=25)
                confirmFrame = tk.Frame(confirm)
                confirmFrame.pack()
                btnBk = ttk.Button(confirmFrame, text="Create backup", command=lambda: self.backup(), style="NStyle.TButton", width=25)
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
                for i in self.listE:
                    key=str("\"" + self.data[str(i)]['path'] + "\"")
                    DefaultHive.add(key=key, value=self.data[str(i)]['key'], type=self.data[str(i)]['type'], data=self.data[str(i)]['states']['enabled'], i=i, jsonData=self.data)
                    if DefaultHive.outputStatus == 0:
                        self.console.config(state="normal")
                        self.console.insert('end', DefaultHive.output + "\n")
                        self.console.config(state="disabled")
                        self.btns[int(i)][str('btnE' + i)].config(style="NStyle.TButton")
                    else:
                        self.console.config(state="normal")
                        self.console.insert('end', DefaultHive.output + "\n", 'warning')
                        self.console.config(state="disabled")
                        self.btns[int(i)][str('btnE' + i)].config(style="NStyle.TButton")
                for i in self.listD:
                    key=str("\"" + self.data[str(i)]['path'] + "\"")
                    DefaultHive.add(key=key, value=self.data[str(i)]['key'], type=self.data[str(i)]['type'], data=self.data[str(i)]['states']['disabled'], i=i, jsonData=self.data)
                    if DefaultHive.outputStatus == 0:
                        self.console.config(state="normal")
                        self.console.insert('end', DefaultHive.output + "\n")
                        self.console.config(state="disabled")
                        self.btns[int(i)][str('btnD' + i)].config(style="NStyle.TButton")
                    else:
                        self.console.config(state="normal")
                        self.console.insert('end', DefaultHive.output + "\n", 'warning')
                        self.console.config(state="disabled")
                        self.btns[int(i)][str('btnD' + i)].config(style="NStyle.TButton")
            else:
                for i in self.listE:
                    self.btns[int(i)][str('btnE' + i)].config(style="NStyle.TButton")
                for i in self.listD:
                    self.btns[int(i)][str('btnD' + i)].config(style="NStyle.TButton")
                self.console.config(state="normal")
                self.console.insert('end', DefaultHive.output + "\n", 'warning')
                self.console.config(state="disabled")


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
            self.listE = []
            self.listD = []
    
        
        def infoBox(self):
            IW = tk.Toplevel()
            IW.title("Application Info")
            IW.geometry('420x200')
            IW.resizable(False, False)
            label = tk.Label(IW, text="Default Registry Modifier version " + ver + "\nCreated by IveMalfunctioned\nPython version " + python_version())
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
        
        def importJson(self):
            newData = askopenfilename(defaultextension=".json")
            if newData:
                newData = newData.replace("/", "\\")
                try:
                    with open(newData, 'r') as file:
                        self.data = json.loads(file.read())
                except:
                    self.console.config(state="normal")
                    self.console.insert('end', "Could not import JSON data: Formatting error\n", 'warning')
                    self.console.config(state="disabled")
                    return
                self.count = 1
                self.listE = []
                self.listD = []
                for i, value in enumerate(self.btns):
                    value["btnE" + str(i)].destroy()
                    value["btnD" + str(i)].destroy()
                    value["btnR" + str(i)].destroy()
                    value["txt" + str(i)].destroy()
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
                self.canvas.configure(scrollregion=(0,0,420+descLength,478+len(self.data)*30))
                self.btns = []
                
                self.addKeyEntries()
                self.console.config(state="normal")
                self.console.insert('end', "Imported JSON data from " + newData + "\n")
                self.console.config(state="disabled")
        
        def useOnlineJson(self):
            try:
                r = requests.get("https://raw.githubusercontent.com/IveMalfunctioned/Default-Registry-Modifier/main/keys.json")
                try:
                    self.data = json.loads(r.text)
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
            self.count = 1
            self.listE = []
            self.listD = []
            for i, value in enumerate(self.btns):
                    value["btnE" + str(i)].destroy()
                    value["btnD" + str(i)].destroy()
                    value["btnR" + str(i)].destroy()
                    value["txt" + str(i)].destroy()
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
            self.canvas.configure(scrollregion=(0,0,420+descLength,478+len(self.data)*30))
            self.btns = []
            
            self.addKeyEntries()
            self.console.config(state="normal")
            self.console.insert('end', "Imported JSON data from GitHub\n")
            self.console.config(state="disabled")
            

        def backup(self, confirm=False):
            if confirm:
                confirm.destroy()
            var = subprocess.check_output("powershell \"[Environment]::GetFolderPath('Desktop')\"", shell=True)
            path = asksaveasfilename(title="Save backup of default user hive", defaultextension=".DAT", initialdir=str(var.decode('utf-8')), initialfile="NTUSER.DAT", filetypes=[("DAT files", "*.DAT"), ("All Files", "*.*")])
            if path:
                path = path.replace("/", "\\")
                copy = subprocess.run(f"copy /v {DefaultHive.path} {path}", shell=True, capture_output=True, text=True)
                if "Access is denied" in copy.stdout:
                    self.console.config(state="normal")
                    self.console.insert('end', f"Could not copy {DefaultHive.path} to {path}. Access was denied\n", 'warning')
                    self.console.config(state="disabled")
                else:
                    self.console.config(state="normal")
                    self.console.insert('end', f"Created backup of {DefaultHive.path} at {path}\n")
                    self.console.config(state="disabled")

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
