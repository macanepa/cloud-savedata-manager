# Cloud SaveData Manager

This application allows you to make cloud backups to the Google Drive Platform 

## Features
- Backup your local SaveData to your own Google Drive Account
- Restore cloud SaveData to your local machine

## Installation Instructions 
When you open the program for the first time, it will guide you with these instructions.
### 1. Obtain Google Drive API Credentials
1. Head to [this link](https://developers.google.com/drive/api/v3/quickstart/python) and click on *Enable the Drive API*
2. Enter a name for the project, e.g *Cloud SaveData Manager*
3. Select *Yes* and *Next*
4. Select *Desktop app* and *Create*
5. Click *Download Client Configuration*
6. Place the *credentials.json* inside the *credentials* folder)

### 2. Login on Google Drive
1. Login with your Google Account
2. Click on *Advanced Configuration* and then on the name of your application defined at *1.2*
3. Allow the required permissions


## Usage
### Upload a New SaveData to the Cloud
To upload a SaveData to Google Cloud, first you must declare the videogame you want to backup.
To do this follow these steps:

1. Select **Backup SaveData to Cloud**
2. Select **Add New Title**
3. Introduce a name for the videogame (this will be the name displayed name on Google Cloud)
4. Introduce the path of the SaveData directory (e.g C:\Users\user\Documents\My Games\Data Directory)

After this, a *zip* files containing the SaveData of the game will be uploaded to your Google Drive.
This data will be located on a new folder called *Cloud SaveData Manager*

### Update a SaveData on the cloud
In case you want to backup a more recent SaveData file of a previously declared videogame,
you may do so following these steps:

1. Select **Backup SaveData to Cloud**
2. Select **Update Existing Title**
3. Select the title you want to update on the cloud
4. When the overwrite message comes up, select **Yes**

### Restore a backup from the cloud to your local machine
Whenever you want to restore the SaveData from the cloud just follow these steps:

1. Select **Restore SaveData from Cloud**
2. Select the title you want to restore from the cloud
3. When the overwrite message comes up, select **Yes**


### Change Google Account
In case you want to start syncing SaveData with another Google Account,
you may do so by following these steps:

1. Select **Settings**
2. Select **Change Sync Account**
3. On the confirmation message, select **Yes**
4. Log-in with the new Google Account

On the main menu, your new Google Account will be displayed on green.
