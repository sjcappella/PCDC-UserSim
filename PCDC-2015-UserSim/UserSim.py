__author__ = 'Sam Cappella'

import socket
import sys
import threading

from Logger import Logger
from WebSim import WebSim
from Pop3Sim import Pop3Sim
from FileShareSim import FileShareSim


# Define main function
def main(argv):
    logger = Logger()
    logger.log("Running main()")

    # Create thread events
    webSimThread = WebSim(logger)
    pop3SimThread = Pop3Sim(logger)
    fileShareThread = FileShareSim(logger)


    # Start threads
    webSimThread.start()
    pop3SimThread.start()
    fileShareThread.start()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ('0.0.0.0', 55555)
    s.bind(address)
    s.listen(5)
    run = True
    result = ""
    while run:
        connection, clientAddress = s.accept()
        command = connection.recv(1024)
        if command == "WEB-TRAFFIC-SCORE":
            result = webSimThread.score()
        if command == "POP3-SCORE":
            result = pop3SimThread.score()
        if command == "FILE-SHARE-SCORE":
            result = fileShareThread.score()
        if command == "STOP":
            webSimThread.stop()
            pop3SimThread.stop()
            fileShareThread.stop()
            logs = logger.finish()
            for log in logs:
                connection.sendall(log)
            run = False
            connection.close()
            continue
        if result == True:
            connection.sendall("SUCCESS")
        else:
            connection.sendall("FAIL")
        connection.close()

    # Join all the threads back
    webSimThread.join()
    pop3SimThread.join()
    fileShareThread.join()


# Setup call to main function
if __name__ == "__main__":
    main(sys.argv)



