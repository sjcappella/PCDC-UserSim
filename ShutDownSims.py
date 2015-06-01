#!/usr/bin/env python

import socket
import sys

def main(argv):
	if len(argv) < 2:
		print("Not enough arguments.")
		sys.exit()

	log_file = "./" + argv[1].replace(".", "-") + "-log.txt"
	log_contents = ""
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		target_address = (argv[1], 55555)
		s.connect(target_address)
		s.sendall("STOP")
		while True:
			data = s.recv(8192)
			if data == "":
				break
			log_contents += data
		s.close()
		f = open(log_file, 'w+')
		f.write(log_contents)
		f.close()
		
	except:
		sys.exit(1)

if __name__ == "__main__":
	main(sys.argv)