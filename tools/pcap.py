import os
import sys
from scapy.all import *

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

def print_raw(frames):
	data = ""
	for frame in frames:
		last = frame.getlayer(Raw)
		if last:
			data += last.load
		#print frame[0].show()

	if data:
		print data
	else:
		print "[!] No raw data."

	#print frame[2].summary()
	#print frame[2].show()
	#data = frame[1].command()


# Function for finding filenames etc in hex encoded frames (e.g. dnscat) 
# Its a PoC so far :^)
def check_dns(frames):
	last_qry = ''
	out = ''
	q_nb = 0

	filetypes = ["png"]
	frametype = [DNSQR, DNSRR]
	for frame in frames:
		for types in frametype:
			if frame.haslayer(types):
				qry = frame[DNSQR].qname('.skullseclabs.org.', '').split('.')
				qry = ''.join(_.decode('hex') for _ in qry)
				for filetype in filetypes:
					if filetype in qry.lower():
						print qry

		#print qry
		#if frame.haslayer(DNSQR) and not frame.haslayer(DNSRR):
			#qry = frame[DNSQR].qname.replace('.skullseclabs.org.', '').split('.')
			#qry = ''.join(_.decode('hex') for _ in qry)

			#if qry == last_qry:
			#	continue
			
		#print '%r' % qry
			#last_qry = qry

	"""
			q_nb += 1

			if q_nb == 7: # packet with PNG header
				out += qry[8:]

			if 7 < q_nb < 127: # All packets up to IEND chunk
				out += qry
	print out
	"""



def run_file(pcap, flag=""):
	r = rdpcap(pcap)	
	print_raw(r)
	check_dns(r)

def setup():
	if len(sys.argv) < 2:
		usage()

	flag = ""
	if len(sys.argv) > 2: 
		flag = sys.argv[2]

	if not check_file_exists():
		print "%s doesn't exist." % sys.argv[1]

	if flag:
		run_file(sys.argv[1], flag=flag)
	else:
		run_file(sys.argv[1], flag)

if __name__ == "__main__":
	setup()
