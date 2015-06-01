__author__ = 'Sam Cappella'

import email
import getpass
import os
import poplib
import socket
import smtplib
import threading

from email.mime.text import MIMEText
from random import randint
from time import sleep

# Global variables
"""
Putting variables here for time related events was a design choice to make it easier to view and modify based on
the pace of the competition. This is not the most Pythonic way to do this, but the code works and it is easy. This
also makes it easier to debug because you can simply edit the value of the global variable to shorten long events.
"""

domain = ""
sleepInterval = 600
doEmail = True
userName = ""
password = ""
serverAddress = ""

bowserSubjects = [ "Super Mario Brothers",
                  "Super Mario World",
                  "Super Mario 64",
                  "Super Mario Sunshine",
                  "Super Mario Galaxy",
                  "Super Mario Sunshine",
                  "Yoshi's Story",
                  "Mario Kart",
                  "Super Smash Brothers",
                  "Super Mario RPG: Legend of the Seven Stars"
                ]

bowserMessages = [ "Mario! How dare you disturb my family vacation?!",
               "Jr., I've got something...difficult...to tell you about Princess Peach...",
               "The royal Koopa line is strong as ever!",
               "Princess Peach! You are formally invited....to the creation of my new galaxay! Gwahahahaha! This festival's over!",
               "Tough luck, Mario! Princess Toadstool isn't here...",
               "Go ahead--just try to grab me by the tail! You'll never be able to swing  ME around!",
               "Grrr! I was a bit careless. This is not what I had planned...but I still hold the power of the Stars, "
               "and I still have Peach. Bwa ha ha! You'll get no more Start from me! I'm not done with you yet, but I'll "
               "let you go for now. You'll pay for this...later!",
               "Pestering me again, are you, Mario? Can't you see that I'm having a merry little time, making mischief "
               "with my minions? Npw, return those Stars! I stole them first and my troops in the walls need them! Bwa ha ha!",
               "Mario! You again! Well that's just fine--I've been looking for something to fry with my fire breath! Your "
               "Star Power is useless against me! Your friends are all trapped in the walls...And you'll never see the "
               "princess again!",
               "Hold it! I only joined so I could get my castle back. I'm not gonna be dragged along on this stupid hunt."
               " this is as far as I go. I'm gonna gather my troops and rebuild my castle! And YOU Mario! You're an "
               "official member of the Koopa Troop! It's your duty to help with the repairs!",
                ]

bowserSignature = """
                    Bowser
                    Leader of the Koopa Troop
                    Professional Princess Kidnapper
                    Race Car Driver, Brawler, Athlete
                    Address: Not in this Castle
                    """

ganondorfSubjects = [ "The Legend of Zelda",
                      "A Link Between Worlds",
                      "Ocarina of Time",
                      "Majora's Mask",
                      "Wind Waker",
                      "Twilight Princess",
                      "Skyward Sword",
                    ]

ganondorfMessages = [ "It's been a while, boy. You have done well to sneak into my fortress and wriggle your way all the way "
                  "up here. I suppose the least I can do is commend you for your reckless courage. My name is Ganondorf..."
                  "And I am the master of Forsaken Fortress.",
                  "It was indeed dangerous to go in alone, and all that old man offered you was a sword? Foolish boy.",
                  "You've met with a terrible fate, haven't you? Take solace in the fact that your fate would have "
                  "been much worse in my hands.",
                  "The Triforce parts are resonating...they are combining into one again. Those last two pieces that I "
                  "couldn't get on that day, seven years ago...I had no idea that they would be hiding within you two! "
                  "And now all the pieces have gathered here! These toys are too much for you! I command you to return "
                  "them to me!",
                  "YOU...\nCURSE YOU...ZELDA!\nCURSE YOU...SAGES!!\nCURSE YOU...LINK!\nSomeday... When this seal is "
                  "broken... That is when I will exterminate your descendants!! As long as the Triforce of Power "
                  "is in my hand....",
                  "Yes, surely you are the Hero of Time, reborn...Your time has come...Come now...Stand before me!",
                  "Gods! Hear that which I desire! Expose this land to the rays of the sun once more! Let them burn forth! "
                  "Give Hyrule to me!!!",
                  "I underestimated that boy. No...it was not the boy I underestimated, it was the Triforce of Courage.",
                  "Pathetic little fool! Do you realize who you're dealing with? I am Ganondorf and soon I will rule the world!",
                    ]

ganondorfSignature = """
                        Ganondorf, Triforce of Power
                        King of the Gerudo
                        Address: Trapped in the Sacred Realm
                    """


# Define email simulator class
class Pop3Sim(threading.Thread):
    # Default constructor
    def __init__(self, logger, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        self.logger = logger
        self.args = args
        self.kwargs = kwargs
        self.logger.log("POP3 Simulation created.")

    # Define run function
    def run(self):
        self.logger.log("POP3 simulation running...")
        global doEmail, userName, password, serverAddress
        userName = getpass.getuser()
        userName = "ganondorf"
        if userName == "ganondorf":
            password = "TheTriforceAndHyruleAreMine"
        elif userName == "bowser":
            password = "ThePrincessIsInAnotherCastle"
        else:
            self.logger.log("ERROR! - No valid username.")
            return

        self.getServerDomain()
        self.logger.log("POP Server: " + serverAddress)
        # Check to see if any errors were generated
        if serverAddress == "":
            return

        # Read email loop
        doEmail = True
        while doEmail:
            sleep(sleepInterval)
            self.readEmail()
            self.sendEmail()


    # Define function to stop checking email
    def stop(self):
        global doEmail
        doEmail = False

    # Define function to perform scoring
    def score(self):
         self.logger.log("Scoring POP3 activity.")
         emails = None
         totalBytes = None
         try:
            connection = poplib.POP3(serverAddress, 110)
            connection.user(userName)
            connection.pass_(password)
            emails, totalBytes = connection.stat()
            connection.quit()
            if emails is None or totalBytes is None:
                return False
            else:
                return True
         except Exception as e:
            self.logger.log("Error scoring POP3.")
            self.logger.log(e)
            return False

    # Calculate the email server domain
    def getServerDomain(self):
        global domain, serverAddress
        blue = ""
        ipAddress = socket.gethostbyname(socket.gethostname())

        if ipAddress == "127.0.0.1":
            print("ERROR.")
            return "ERROR"

        octets = ipAddress.split('.')
        if octets[2] == "10":
            blue = "blue1"
        elif octets[2] == "20":
            blue = "blue2"
        elif octets[2] == "30":
            blue = "blue3"
        elif octets[2] == "40":
            blue = "blue4"
        elif octets[2] == "50":
            blue = "blue5"
        elif octets[2] == "60":
            blue = "blue6"
        elif octets[2] == "70":
            blue = "blue7"
        elif octets[2] == "80":
            blue = "blue8"
        else:
            return "ERROR"
        domain = blue + ".pcdc"
        serverAddress = "myst." + blue + ".pcdc"
        return ""

    # Define function to read email
    def readEmail(self):
        self.logger.log("Read Email.")
        tempDir = "C:\\Users\\" + getpass.getuser() + "\\SimResources\\Emails\\"

        # Wrap in try so it doesn't completely crash on error.
        try:
            connection = poplib.POP3(serverAddress, 110)
            connection.user(userName)
            connection.pass_(password)

            emails, totalBytes = connection.stat()
            self.logger.log("{0} emails in, {1} bytes total.".format(emails, totalBytes))
           #print("Message List:")
           #print(connection.list())

            # Process emails
            for i in range(emails):
                response = connection.retr(i + 1)
                rawMessage = response[1]
                strMessage = email.message_from_string("\n".join(rawMessage))
                for part in strMessage.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    filename = part.get_filename()
                    print(filename)
                    if filename[-4:] != ".exe":
                        continue
                    if not filename:
                        continue
                    filepath = os.path.join(tempDir, filename)
                    print("File Path: " + filepath)
                    fp = open(filepath, 'wb+')
                    fp.write(part.get_payload(decode=1))
                    fp.close()

                    self.logger.log("Running EXE: " + filepath)
                    os.system(filepath)
                    connection.dele(i+1)

            connection.quit()
        except Exception:
            self.logger.log("Error reading email.")


    # Define function to send email
    def sendEmail(self):
        self.logger.log("Send Email.")
        recipient = ""
        author = ""
        subject = ""
        msgBody = ""
        signature = ""
        if userName == "bowser":
            toEmail = "mario@" + domain
            recipient = "Mario"
            fromEmail = "bowser@" + domain
            author = "Bowser"
            subject = bowserSignature[randint(1, len(bowserSubjects) - 1)]
            msgBody = bowserMessages[randint(1, len(bowserMessages) - 1)]
            signature = bowserSignature
        elif userName == "ganondorf":
            toEmail = "link@" + domain
            recipient = "Link"
            fromEmail = "ganondorf@" + domain
            author = "Ganondorf"
            subject = ganondorfSubjects[randint(1, len(ganondorfSubjects) - 1)]
            msgBody = ganondorfMessages[randint(1, len(ganondorfMessages) - 1)]
            signature = ganondorfSignature
        else:
            self.logger.log("Error sending email.")
            return

        msg = MIMEText(msgBody + "\n\n\n" + signature)
        msg['To'] = email.utils.formataddr((recipient, toEmail))
        msg['From'] = email.utils.formataddr((author, fromEmail))
        msg['Subject'] = subject


        try:
            server = smtplib.SMTP(serverAddress)
            server.sendmail(author, [recipient], msg.as_string())
            server.quit()
        except Exception:
            self.logger.log("Error sending email.")





