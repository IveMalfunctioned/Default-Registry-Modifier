import subprocess

global data

class Hive:
    def __init__(self, path):
        self.path = path
        self.output = ""
        self.outputStatus = 0
    
    def path(self):
        return str(self.path)

    def load(self):
        proc = subprocess.run(f"reg load HKEY_USERS\\Default {self.path}", shell=True, capture_output=True)
        if proc.returncode == 0:
            self.output = "Default hive loaded to HKEY_USERS\\Default"
            self.outputStatus = 0
            return self.output, self.outputStatus
        elif proc.returncode == 1:
            self.output = "Could not load hive, make sure the file is not being used by any processes and another hive is not loaded at HKEY_USERS\\Default"
            self.outputStatus = 1
            return self.output, self.outputStatus
        else:
            self.output = "Unknown error loading hive"
            self.outputStatus = 1
            return self.output, self.outputStatus
    
    def unload(self):
        proc = subprocess.run(f"reg unload HKEY_USERS\\Default", shell=True, capture_output=True)
        if proc.returncode == 0:
            self.output = "Unloaded hive at HKEY_USERS\\Default"
            self.outputStatus = 0
            return self.output, self.outputStatus
        elif proc.returncode == 1:
            self.output = "Could not unload hive, make sure it's not being used by any processes"
            self.outputStatus = 1
            return self.output, self.outputStatus
        else:
            self.output = "Unknown error unloading hive"
            self.outputStatus = 1
            return self.output, self.outputStatus
    
    def add(self, key, value, type, data, i, jsonData):
        self.key = key
        self.value = value
        self.type = type
        self.data = data
        self.jsonData = jsonData
        proc = subprocess.run(f"reg add {self.key} /v {self.value} /t {self.type} /d {str(self.data)} /f", shell=True, capture_output=True)
        if proc.returncode == 0:
            self.output = "Added " + str(self.jsonData[str(i)]['displayname']) + " key with disabled value to the default registry"
            self.outputStatus = 0
            return self.output, self.outputStatus
        elif proc.returncode == 1:
            self.output = f"Error adding key {str(self.jsonData[str(i)]['displayname'])} to the default registry, make sure you have permission to write to this key"
            self.outputStatus = 1
            return self.output, self.outputStatus
        else:
            self.output = "Unknown error adding key to the default registry"
            self.outputStatus = 1
            return self.output, self.outputStatus