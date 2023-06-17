import tkinter as tk
from tkinter import ttk
from classes import Hive, jsonDl, data
import ctypes, os

def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

if isAdmin():

    keys = jsonDl(data)
    DefaultHive = Hive(path="%SystemDrive%\\Users\\Default\\NTUSER.DAT")

    class MainApp:
        def __init__(self, window, data):
            self.window = window
            self.data = data

            self.listE = []
            self.listD = []

            menubar = tk.Menu(window)
            filemenu = tk.Menu(menubar, tearoff=0)
            filemenu.add_command(label="Save changes", command=self.commitConfirm)
            menubar.add_cascade(label="Menu", menu=filemenu)
            window.config(menu=menubar)

            self.btns = []
            self.canvas = tk.Canvas(window,scrollregion=(0,0,420,478+len(data)*30), highlightthickness=0)
            self.canvas.config(width=420, height=476)
            self.canvas.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(event.delta / -60), "units"))
            self.sbar = ttk.Scrollbar(window, orient="vertical", command=self.canvas.yview)
            self.canvas.config(yscrollcommand=self.sbar.set)
            self.sbar.place(relx=1,rely=0,relheight=.6,anchor="ne")
            self.frame = tk.Frame(self.canvas)
            self.canvas.create_window((0, 0), window=self.frame, anchor=tk.NW)
            self.console = tk.Text(
                window,
                height = '20',
                width = window.winfo_reqwidth()
            )
            self.console.insert("end", "Default Registry Modifier version 1.0 - Console log\n\n")
            self.console.config(state="disabled")
            self.addKeyEntries()
            self.canvas.pack(fill="both")
            self.console.pack(side="bottom")

            HStyle = ttk.Style()
            HStyle.configure("HStyle.TButton", background="#0000FF")
            NStyle = ttk.Style()
            NStyle.configure("NStyle.TButton", background="gray")
        
        def addKeyEntries(self):
            count = 1
            for i in self.data:
                inframe = tk.Frame(self.frame)
                inframe.pack(fill="x")

                txt = ttk.Label(inframe, text=str(count) + ": " + data[str(i)]['displayname'] + "\nDescription: " + data[str(i)]['description'], anchor="w")
                txt.pack(anchor="w", padx=10, pady=(10,5))

                btnE = ttk.Button(inframe, text="Enable", style="NStyle.TButton", command=lambda i=i: self.enable(i))
                btnE.pack(side="left", padx=(20, 3))

                btnD = ttk.Button(inframe, text="Disable", style="NStyle.TButton", command=lambda i=i: self.disable(i))
                btnD.pack(side="left")

                btnR = ttk.Button(inframe, text="Remove", style="NStyle.TButton", command=lambda i=i: self.remove(i))
                btnR.pack(side="left", padx=3)

                self.btns.append({"btnE" + str(i): btnE, "btnD" + str(i): btnD, "btnR" + str(i): btnR})
                count += 1
        
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
        
        def commitConfirm(self,):
            confirm = tk.Toplevel()
            confirm.title("Confirmation")
            confirm.geometry('420x200')
            confirm.resizable(False, False)
            infotxt = tk.Label(confirm, text="Apply tweaks to default user? Program currently doesn't support backups,\nso do this at your own risk or create a backup of\nC:\\Users\\Default\\NTUSER.DAT")
            infotxt.pack()
            btnY = tk.Button(confirm, text="Yes", command=lambda: self.commit(confirm), width=3, height=1)
            btnY.pack(side="left", padx=(170, 8))
            btnN = tk.Button(confirm, text="No", command=confirm.destroy, width=3, height=1)
            btnN.pack(side="left")
        
        def commit(self, confirm):
            confirm.destroy()
            if not self.listE and not self.listD:
                self.console.config(state="normal")
                self.console.insert('end', "Must select values!\n")
                self.console.config(state="disabled")
            else:
                DefaultHive.load()
                self.console.config(state="normal")
                self.console.insert('end', "Default hive loaded to HKEY_USERS\\Default\n")
                self.console.config(state="disabled")
                for i in self.listE:
                    key=str("\"" + data[str(i)]['path'] + "\"")
                    DefaultHive.add(key=key, value=data[str(i)]['key'], type=data[str(i)]['type'], data=data[str(i)]['states']['enabled'])
                    self.console.config(state="normal")
                    self.console.insert('end', "Added " + str(data[str(i)]['key']) + " with enabled value to the default registry\n")
                    self.console.config(state="disabled")
                    self.btns[int(i)][str('btnE' + i)].config(style="NStyle.TButton")
                self.listE = []
                for i in self.listD:
                    key=str("\"" + data[str(i)]['path'] + "\"")
                    DefaultHive.add(key=key, value=data[str(i)]['key'], type=data[str(i)]['type'], data=data[str(i)]['states']['disabled'])
                    self.console.config(state="normal")
                    self.console.insert('end', "Added " + str(data[str(i)]['displayname']) + " key with disabled value to the default registry\n")
                    self.console.config(state="disabled")
                    self.btns[int(i)][str('btnD' + i)].config(style="NStyle.TButton")
                DefaultHive.unload()
                self.console.config(state="normal")
                self.console.insert('end', "Unloaded hive at HKEY_USERS\\Default\n")
                self.console.insert('end', "Completed\n\n")
                self.console.config(state="disabled")

    window = tk.Tk()
    window.geometry('420x800')
    window.resizable(False, False)
    window.title("Default Registry Modifier")
    window.iconbitmap(default="icon.ico")
    main = MainApp(window, data)
    window.mainloop()

else:
    window = tk.Tk()
    window.geometry('350x100')
    window.resizable(False, False)
    window.title("Program needs admin privileges")
    label = tk.Label(window, text="This script requires administrator privileges to run.\nPlease rerun the program as administrator and try again")
    label.pack()
    button = tk.Button(window, text="Exit", command=window.destroy)
    button.pack()
    window.mainloop()