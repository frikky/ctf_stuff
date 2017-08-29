import os
import sys
import scapy

def usage():
	sys.stdout.write(
		"[!] Error: Missing pcap.\n"
		"[?] Usage: python pcap.py <pcap filepath>\n"
	)
	exit()

def check_file_exists():
	try:
		os.stat(sys.argv[1])	
		return True
	except OSError:
		return False

def setup():
	if len(sys.argv) < 2:
		usage()

	if not check_file_exists():
		print "%s doesn't exist." % sys.argv[1]

	#run_file(sys.argv[1])

if __name__ == "__main__":
	setup()
