import sys
import json
import requests

class config:
	HEADER = '\033[95m'
	WARNING = '\033[93m'
	ENDC = '\033[0m'
	timeout=5
	filters = [
		"content-Length",
		"cache-control",
		"date",
		"set-cookie"
	]
	paths = [
		"robots.txt",
		".git",
	]

config = config()

def find_paths(url):
	sys.stdout.write("\n%s--- Paths ---%s\n" % (config.WARNING, config.ENDC))
	for path in config.paths:
		full_url = "%s/%s" % (url, path)
		req = requests.get(full_url, timeout=config.timeout)
		if req.ok:
			sys.stdout.write("%s: %s\n" % (path, str(req.status_code)))

def print_headers(session):
	sys.stdout.write("\n%s--- Headers ---%s\n" % (config.WARNING, config.ENDC))
	for item in dict(session.headers):
		if item.lower() not in config.filters:
			sys.stdout.write("%s: %s\n" % (item, session.headers[item]))

	# Verify cookies
def print_cookies(session):
	cookies = ""
	try:
		cookies = dict(session.headers)["Set-Cookie"]
	except KeyError:
		try:
			cookies = dict(session.headers)["set-cookie"]
		except KeyError:
			pass

	if cookies:
		sys.stdout.write(config.WARNING +"\n%s--- Cookies ---%s\n" % (config.WARNING, config.ENDC))
		sys.stdout.write("%s\n" % "\n".join(cookies.split(";")))

# FIX - change to session ???
def create_session(url):
	# Tests the initial connection
	try:
		session = requests.get(url, timeout=config.timeout)
	except requests.exceptions.ConnectTimeout:
		sys.stdout.write("[!] URL not available.\n")
		exit()
	except KeyboardInterrupt:
		sys.stdout.write("\n[!] Pressed ctrl+C\n")
		exit()
		
	return session

def fix_url(url):
	if not url.startswith("http://") and not url.startswith("https://"):
		tmpurl = "http://%s" % url
	else:
		tmpurl = url

	url = "/".join(tmpurl.split("/")[:3])
		
	return url

def usage():
	sys.stdout.write(
		"[!] Error: Missing url argument.\n"
		"[?] Usage: python web.py <url>\n"
	)
	exit()

def runscanner():
	if len(sys.argv) < 2:
		usage()

	url = fix_url(sys.argv[1])

	session = create_session(url)
	if not session.ok:
		sys.stdout.write("[!] URL not available.\n")
		exit()

	print_headers(session)
	print_cookies(session)
	find_paths(url)

if __name__ == "__main__":
	runscanner()
