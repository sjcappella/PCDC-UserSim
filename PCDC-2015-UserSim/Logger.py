__author__ = 'Sam Cappella'

import getpass

from datetime import datetime

logFile = "C:\\Users\\" + getpass.getuser() + "\\SimResources\\logfile.txt"
messages = []

# Define logger class
class Logger:
    # Default constructor
    def __init__(self):

        try:
            file = open(logFile, "w+")
            file.write("======================================\n")
            file.write("[*] Logging started at " + str(datetime.now()) + "\n")
            file.close()
        except:
            pass

    # Define log function
    def log(self, logMessage):
        try:
            global messages
            messages.append(str(logMessage))
            if len(messages) >= 5:
                with open(logFile, 'a') as f:
                    for message in messages:
                        f.write("[ " + str(datetime.now()) + " ][*] " + str(message) + "\n")
                f.close()
                messages = []
        except:
            pass


    # Define a function to flush all messages to file
    def flush(self):
        try:
            global messages
            with open(logFile, 'a') as f:
                for message in messages:
                    f.write("[ " + str(datetime.now()) + " ][*] " + str(message) + "\n")
                messages = []
        except:
            pass

    # Define the finish function
    def finish(self):
        try:
            self.flush()
            with open(logFile) as f:
                content = f.readlines()
            return content
        except:
            pass



