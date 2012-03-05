import os,subprocess,socket
def pm_uptime(bot,parts):
	"""Check system uptime"""
	return os.popen('uptime').read().strip()
def pm_fortune(bot,parts):
	"""Check system uptime"""
        if "-o" in parts[3]:
            return subprocess.Popen(['fortune', "-o"],stdin = subprocess.PIPE,stderr = subprocess.STDOUT,stdout = subprocess.PIPE).stdout.read().rstrip().replace("\t","    ")
        else:
            return subprocess.Popen('fortune',stdin = subprocess.PIPE,stderr = subprocess.STDOUT,stdout = subprocess.PIPE).stdout.read().rstrip().replace("\t","    ")
def pm_fig(bot,parts):
	"""Figlet addon"""
	return subprocess.Popen(['figlet', parts[3].split(" ",1)[1]],stdin = subprocess.PIPE,stderr = subprocess.STDOUT,stdout = subprocess.PIPE).stdout.read().rstrip() + "\n "
def pm_random(bot,parts):
	"""Returns a 100 character random string"""
	a = open("/dev/urandom","r")
	str = a.read(100)
	a.close()
	return str
def pm_nslookup(bot,parts):
	try:
		return socket.gethostbyname(parts[3][1:].split()[-1])
	except:
		return "Cannot find " + parts[3][1:].split()[-1]
def pm_dbusers(bot,parts):
	import _mysql
	db = _mysql.connect(host=self.database["hostname"], port=self.database["port"], user=self.database["user"], passwd=self.database["password"], db=self.database["database"])
	db.query("select * from information_schema.processlist")
	db.close()
	r = db.store_result()
	a = r.fetch_row()
	return str(len(a)) + " active connections."
def pm_temp(bot,parts):
	a = open("/proc/acpi/thermal_zone/THM/temperature")
	b = a.read()
	a.close()
	return "temp: " + b.split()[-2] + " C"

