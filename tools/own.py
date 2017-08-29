import pwn
import sys

"""
	RUN CODE in exploit() 
"""

def usage():
	sys.stdout.write(
		"[!] Error: Missing url/ip and port.\n"
		"[?] Usage: python own.py <url/ip> <port>\n"
	)
	exit()

def exploit(target):
	# When to stop
	target.recvuntil('\n')

	while True:
		# Get lines 
		line = target.recvline(keepends=False)
		# *** Do something with data here ***
			
		data = ""
		# Send data
		target.send(data)

def setup():
	if len(sys.argv) < 3:
		usage()

	try:
		target = pwn.remote(sys.argv[1], sys.argv[2])
	except pwn.pwnlib.exception.PwnlibException:
		sys.stdout.write("[!] %s:%s not available.\n" % (sys.argv[1], sys.argv[2]))
		exit()
	except ValueError:
		sys.stdout.write("[!] \'%s\' is not a port.\n" % sys.argv[2])
		exit()
		
	exploit(target)

if __name__ == "__main__":
	setup()
