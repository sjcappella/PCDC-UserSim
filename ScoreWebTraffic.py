#!/usr/bin/env python

import socket
import sys

def main(argv):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		target_address = (argv[1], 55555)
		s.connect(target_address)
		s.sendall("WEB-TRAFFIC-SCORE")
		response = s.recv(1024)
		s.close()
		print("Response: " + str(response))
		if response == "SUCCESS":
			sys.exit(0)
		else:
			sys.exit(1)
	except:
		sys.exit(1)

if __name__ == "__main__":
	main(sys.argv)