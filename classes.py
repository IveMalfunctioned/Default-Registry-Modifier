import requests
import json
import os

global data

r = requests.get("https://raw.githubusercontent.com/IveMalfunctioned/Default-Registry-Modifier/main/keys.json")
data = json.loads(r.text)

#with open("G:\Desktop\Default Registry Modifier\keys.json", "r") as file:
#    data = json.loads(file.read())

class Hive:
    def __init__(self, path):
        self.path = path
    
    def path(self):
        return str(self.path)

    def load(self):
        os.system(f"reg load HKEY_USERS\\Default {self.path}")
    
    def unload(self):
        os.system(f"reg unload HKEY_USERS\\Default")
    
    def add(self, key, value, type, data):
        self.key = key
        self.value = value
        self.type = type
        self.data = data
        os.system(f"reg add {self.key} /v {self.value} /t {self.type} /d {str(self.data)} /f")

class jsonDl:
    def __init__(self, data):
        for key in data:
            setattr(self, data[key]['key'], data[key])
    
    def list(self):
        keysList = []
        for key in data:
            keysList.append(data[key]['displayname'])
        return keysList