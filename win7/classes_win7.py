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
        elif proc.returncode == 1:
            self.output = "Could not load hive, make sure the file is not being used by any processes and another hive is not loaded at HKEY_USERS\\Default"
            self.outputStatus = 1
        else:
            self.output = "Unknown error loading hive"
            self.outputStatus = 1
        return self.output, self.outputStatus
    
    def unload(self):
        proc = subprocess.run(f"reg unload HKEY_USERS\\Default", shell=True, capture_output=True)
        if proc.returncode == 0:
            self.output = "Unloaded hive at HKEY_USERS\\Default"
            self.outputStatus = 0
        elif proc.returncode == 1:
            self.output = "Could not unload hive, make sure it's not being used by any processes"
            self.outputStatus = 1
        else:
            self.output = "Unknown error unloading hive"
            self.outputStatus = 1
        return self.output, self.outputStatus
    
    def add(self, key, i, jsonData, dataType, type=None, valueName=None, data=None, value=None):
        self.key = key
        self.value = value
        self.type = type
        self.data = data
        self.jsonData = jsonData
        self.dataType = dataType
        if dataType == "OnOrOffV" or dataType == "OnOrOffMV":
            proc = subprocess.run(f"reg add {self.key} /v {self.value} /t {self.type} /d {str(self.data)} /f", shell=True, capture_output=True)
            if proc.returncode == 0:
                self.output = "Added " + str(self.jsonData[str(i)]['displayname']) + " key with " + valueName + " value to the default registry"
                self.outputStatus = 0
            elif proc.returncode == 1:
                self.output = f"Error adding key {str(self.jsonData[str(i)]['displayname'])} to the default registry, make sure you have permission to write to this key"
                self.outputStatus = 1
            else:
                self.output = f"Unknown error adding key {str(self.jsonData[str(i)]['displayname'])} to the default registry"
                self.outputStatus = 1
            return self.output, self.outputStatus
        elif dataType == "OnOrOffK":
            if valueName == "disabled" and self.jsonData[str(i)]['values']['disabled'] == "Delete the key":
                self.delete(self.key, valueName=valueName)
            elif valueName == "enabled" and self.jsonData[str(i)]['values']['enabled'] == "Delete the key":
                self.delete(self.key, valueName=valueName)
            else:
                proc = subprocess.run(f"reg add {self.key} /f", shell=True, capture_output=True)
                if proc.returncode == 0:
                    self.output = "Added " + str(self.jsonData[str(i)]['displayname']) + " with " + valueName + " value to the default registry"
                    self.outputStatus = 0
                elif proc.returncode == 1:
                    self.output = "Error adding key " + str(self.jsonData[str(i)]['displayname']) + " to the default registry, make sure you have permission to write to this key"
                    self.outputStatus = 1
                else:
                    self.output = f"Unknown error adding key {str(self.jsonData[str(i)]['displayname'])} to the default registry"
                    self.outputStatus = 1
            return self.output, self.outputStatus
        elif dataType == "String":
            proc = subprocess.run(f"reg add {self.key} /v {self.value} /t {self.type} /d {str(self.data)} /f", shell=True, capture_output=True)
            if proc.returncode == 0:
                self.outputStatus = 0
                self.output = "Added " + str(self.jsonData[str(i)]['displayname']) + " with custom string to the default registry"
            elif proc.returncode == 1:
                self.output = "Error adding key " + str(self.jsonData[str(i)]['displayname']) + " to the default registry, make sure you have permission to write to this key"
                self.outputStatus = 1
            else:
                self.output = f"Unknown error adding key {str(self.jsonData[str(i)]['displayname'])} to the default registry"
                self.outputStatus = 1
            return self.output, self.outputStatus
    
    def delete(self, key, value=None, valueName=None):
        self.key = key
        self.value = value
        if self.value:
            check = subprocess.run(f"reg query {self.key}", shell=True, capture_output=True)
            if check.returncode == 1:
                self.output = f"Key {valueName} already disabled"
                self.outputStatus = 0
                return self.output, self.outputStatus
            elif check.returncode == 0:
                proc = subprocess.run(f"reg delete {self.key} /v {self.value} /f", shell=True, capture_output=True)
                if proc.returncode == 0:
                    self.output = f"Deleted key {self.key}"
                    self.outputStatus = 0
                elif proc.returncode == 1:
                    self.output = f"Error deleting key {self.key}\\{self.value}"
                    self.outputStatus = 1
                else:
                    self.output = f"Unknown error deleting key {self.key}\\{self.value}"
                    self.outputStatus = 1
        elif not self.value:
            check = subprocess.run(f"reg query {self.key}", shell=True, capture_output=True)
            if check.returncode == 1:
                self.output = f"Key {valueName} already disabled"
                self.outputStatus = 0
                return self.output, self.outputStatus
            elif check.returncode == 0:
                proc = subprocess.run(f"reg delete {self.key} /f", shell=True, capture_output=True)
                if proc.returncode == 0:
                    self.output = f"Deleted key {self.key}"
                    self.outputStatus = 0
                elif proc.returncode == 1:
                    self.output = f"Error deleting key {self.key}"
                    self.outputStatus = 1
                else:
                    self.output = f"Unknown error deleting key {self.key}"
                    self.outputStatus = 1
        return self.output, self.outputStatus
