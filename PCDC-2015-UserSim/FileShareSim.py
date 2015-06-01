__author__ = 'Sam Cappella'

import getpass
import os
import shutil
import threading
import uuid

from datetime import datetime
from random import randint
from time import sleep

# Global variables
"""
Putting variables here for time related events was a design choice to make it easier to view and modify based on
the pace of the competition. This is not the most Pythonic way to do this, but the code works and it is easy. This
also makes it easier to debug because you can simply edit the value of the global variable to shorten long events.
"""

remoteFiles = ""
uploadResourcesDirectory = ""
downloadResourcesDirectory = ""
sleepInterval = 120
shareFiles = True

# Define email simulator class
class FileShareSim(threading.Thread):
    # Default constructor
    def __init__(self, logger, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        self.logger = logger
        self.args = args
        self.kwargs = kwargs
        self.logger.log("File Share Simulation created.")

    # Define run function
    def run(self):
        self.logger.log("File Share simulation running...")

        global remoteFiles, uploadResourcesDirectory, downloadResourcesDirectory
        userName = getpass.getuser()
        remoteFiles = "Z:\\SimResources\\" + userName + "\\Files\\"
        uploadResourcesDirectory = "C:\\Users\\" + userName + "\\SimResources\\Uploads\\"
        downloadResourcesDirectory = "C:\\Users\\" + userName + "\\SimResources\\Downloads\\"

        global shareFiles

        # Loop to perform file share activity
        while shareFiles:
            sleep(sleepInterval)
            action = randint(1, 2)
            if action == 1:
                self.uploadFile()
            else:
                self.downloadFile()
            pass

    # Stop file share activity
    def stop(self):
        global shareFiles
        shareFiles = False

    # Function to score the file share activity
    def score(self):
        self.logger.log("Scoring File Share activity.")
        try:
            with open(remoteFiles + "score.txt", 'r') as f:
                line = f.readline()
                if not "score-bot-readme" in line:
                    return False
            fileName = str(uuid.uuid1())
            file = open(remoteFiles + fileName + ".txt", 'w+')
            self.logger.log("Creating score event file: " + remoteFiles + fileName + ".txt")
            file.write("Scorebot-Event-" + str(datetime.now()))
            file.close()
            return True
        except Exception as e:
            self.logger.log("Error scoring file share.")
            self.logger.log(e)
            return False

    # Upload a file
    def uploadFile(self):
        self.logger.log("Upload file.")
        try:
            filesToUpload = os.listdir(uploadResourcesDirectory)
            #print("[* DEBUG *] Potential file uploads:")
            #print(filesToUpload)
            fileIndex = randint(0, len(filesToUpload) - 1)
            fileToUpload = filesToUpload[fileIndex]
            extension = fileToUpload[-4:]
            if os.path.isfile(uploadResourcesDirectory + fileToUpload) is False:
                self.logger.log(uploadResourcesDirectory + fileToUpload + " is not a valid file.")
                return
            self.logger.log("File to upload: " + uploadResourcesDirectory + fileToUpload)
            shutil.copy(uploadResourcesDirectory + fileToUpload, remoteFiles)
            fileUuidName = str(uuid.uuid1())
            self.logger.log("Renaming file " + remoteFiles + fileToUpload + " to " + remoteFiles + fileUuidName + extension)
            os.rename(remoteFiles + fileToUpload, remoteFiles + fileUuidName + extension)
        except Exception as e:
            self.logger.log("Error uploading file.")
            self.logger.log(e)


    # Download a file
    def downloadFile(self):
        self.logger.log("Download file.")
        try:
            filesToDownload = os.listdir(remoteFiles)
            print("[* DEBUG *] Potential file downloads:")
            print(filesToDownload)
            fileIndex = randint(0, len(filesToDownload))
            fileToDownload = filesToDownload[fileIndex]
            # Not fool proof, but we're lazy
            extension = fileToDownload[-4:]
            if os.path.isfile(remoteFiles + fileToDownload) is False:
                self.logger.log(remoteFiles + fileToDownload + " is not a valid file.")
                return
            self.logger.log("File to download: " + remoteFiles + fileToDownload)
            shutil.copy(remoteFiles + fileToDownload, downloadResourcesDirectory)
            fileUuidName = str(uuid.uuid1())
            self.logger.log("Renaming file " + downloadResourcesDirectory + fileToDownload + " to " + downloadResourcesDirectory + fileUuidName + extension)
            os.rename(downloadResourcesDirectory + fileToDownload, downloadResourcesDirectory + fileUuidName + extension)
        except Exception as e:
            self.logger.log("Error downloading file.")
            self.logger.log(e)