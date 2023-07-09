# Default Registry Modifier
Default Registry Modifier is a simple GUI based tool for Windows made in Python using the Tkinter library. It pulls a list of registry keys from online JSON data & lists them with options for enabling or disabling them within the Default user's registry. All tweaks apply to new users upon creation after the use of this tool.

# Screenshot
![image](https://github.com/IveMalfunctioned/Default-Registry-Modifier/assets/20033421/f96f4a9a-3393-4798-8024-e4ba3b45cbc2)

# Usage / download

In order to use this program, download one of the precompiled binaries from the [releases tab](https://github.com/IveMalfunctioned/Default-Registry-Modifier/releases/latest) or compile it. A `main.spec` file is provided for compiling using PyInstaller.

The program requires administrative privileges to run, so make sure you right click the exe and click "Run as administrator".

Enable or disable the desired tweaks (If you changed your mind about modifying one, click "remove" and it won't be modified). Once you've finished, open the `Menu` tab and click `Save changes`. Read the warning and decide on making your confirmation. It will then apply all selected tweaks to the default user, making it so that next time a user is created these settings are default.

# How it works

The program pulls a list of registry keys from [some online JSON data hosted in this GitHub repo](https://github.com/IveMalfunctioned/Default-Registry-Modifier/releases/latest). It goes through it and creates an entry for each one with labels & buttons to enable or disable it. Clicking enable or disable adds the selected tweak to a list for enabling or disabling - of which is gone through upon confirming you want to save the changes. One of the planned QOL features is being able to import offline JSON data. This means that you can download `keys.json` from this repo or modify it/create your own. Speaking of which:

# Other features:
- Create backups
- Import offline JSON data/Re-download online JSON data

# To do list:
- Add the ability to apply these tweaks to the current user, any specified user, or all users
- Add command line options
- Add manual key input
- Add update checking

For more direct information or updates on the project, join the [Windows Modding Discord](https://discord.gg/hzScjC9re6)
