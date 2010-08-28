#this module needs db creation constructor.
import socket, _mysql
def start(bot):
	if not "ip" in bot.registry:
		bot.registry["ip"] = {}
	for user in dbgetall():
		nick = user[0]
		ip = user[1].split(".")
		if not ip[0] in bot.registry["ip"]:
			bot.registry["ip"][ip[0]] = {}
		if not ip[1] in bot.registry["ip"][ip[0]]:
			bot.registry["ip"][ip[0]][ip[1]] = {}
		if not ip[2] in bot.registry["ip"][ip[0]][ip[1]]:
			bot.registry["ip"][ip[0]][ip[1]][ip[2]] = {}
		if not ip[3] in bot.registry["ip"][ip[0]][ip[1]][ip[2]]:
			bot.registry["ip"][ip[0]][ip[1]][ip[2]][ip[3]] = []
		if not nick in bot.registry["ip"][ip[0]][ip[1]][ip[2]][ip[3]]:
			bot.registry["ip"][ip[0]][ip[1]][ip[2]][ip[3]].append(nick)
def cmd_userinit(bot,parts):
	ip = socket.gethostbyname(parts[3].split()[2])
	nick = parts[1]
	dbinsert(nick,ip)
	ip = ip.split(".")
	if not ip[0] in bot.registry["ip"]:
		bot.registry["ip"][ip[0]] = {}
	if not ip[1] in bot.registry["ip"][ip[0]]:
		bot.registry["ip"][ip[0]][ip[1]] = {}
	if not ip[2] in bot.registry["ip"][ip[0]][ip[1]]:
		bot.registry["ip"][ip[0]][ip[1]][ip[2]] = {}
	if not ip[3] in bot.registry["ip"][ip[0]][ip[1]][ip[2]]:
		bot.registry["ip"][ip[0]][ip[1]][ip[2]][ip[3]] = []
	if not nick in bot.registry["ip"][ip[0]][ip[1]][ip[2]][ip[3]]:
		bot.registry["ip"][ip[0]][ip[1]][ip[2]][ip[3]].append(nick)
def cmd_nick(bot,parts):
	nick = parts[2].lower()
	ip = socket.gethostbyname(bot.registry["nicks"][nick]["host"])
	dbinsert(nick,ip)
	ip = ip.split(".")
	if not ip[0] in bot.registry["ip"]:
		bot.registry["ip"][ip[0]] = {}
	if not ip[1] in bot.registry["ip"][ip[0]]:
		bot.registry["ip"][ip[0]][ip[1]] = {}
	if not ip[2] in bot.registry["ip"][ip[0]][ip[1]]:
		bot.registry["ip"][ip[0]][ip[1]][ip[2]] = {}
	if not ip[3] in bot.registry["ip"][ip[0]][ip[1]][ip[2]]:
		bot.registry["ip"][ip[0]][ip[1]][ip[2]][ip[3]] = []
	if not nick in bot.registry["ip"][ip[0]][ip[1]][ip[2]][ip[3]]:
		bot.registry["ip"][ip[0]][ip[1]][ip[2]][ip[3]].append(nick)
def pm_buildipdatabase(bot,parts):
	pass
def pm_ip(bot,parts):
	nick = parts[3].split()[-1].lower()
	if not nick in bot.registry["nicks"]:
		if "." in nick:
			ip = nick.split(".")
			if len(ip) != 4:
				return "No such nick"
		else:
			return "No such nick"
	else:
		ip = socket.gethostbyname(bot.registry["nicks"][nick]["host"]).split(".")
	same = bot.registry["ip"][ip[0]][ip[1]][ip[2]][ip[3]]
	try:
		same.remove(nick)
	except:
		pass
	classc = []
	classb = []
	for x in bot.registry["ip"][ip[0]][ip[1]][ip[2]]:
		for y in bot.registry["ip"][ip[0]][ip[1]][ip[2]][x]:
			if y not in same:
				classc.append(y)
	for x in bot.registry["ip"][ip[0]][ip[1]]:
		for y in bot.registry["ip"][ip[0]][ip[1]][x]:
			for z in bot.registry["ip"][ip[0]][ip[1]][x][y]:
				if z not in same and z not in classc:
					classb.append(z)
	retvar = ""
	if same:
		retvar += "Same IP: " + ", ".join(same) + "\n"
	if classc:
		retvar += "Class C: " + ", ".join(classc) + "\n"
	if classb:
		retvar += "Class B: " + ", ".join(classb)
	if not retvar:
		return "No other nicks"
	else:
		return retvar
def dbinsert(nick,ip):
	db = _mysql.connect(host=bot.database["hostname"], port=bot.database["port"], user=bot.database["user"], passwd=bot.database["password"], db=bot.database["database"])
	db.query("SELECT count(*) FROM iplog WHERE nick='" + _mysql.escape_string(nick) + "' AND ip='" + _mysql.escape_string(ip) + "';")
	total = db.store_result().fetch_row()[0][0]
	if total == "0":
		db.query("INSERT INTO iplog (nick, ip) VALUES ('" + _mysql.escape_string(nick) + "', '" + _mysql.escape_string(ip) + "');")
	db.close()
def dbgetall():
	db = _mysql.connect(host=bot.database["hostname"], port=bot.database["port"], user=bot.database["user"], passwd=bot.database["password"], db=bot.database["database"])
	db.query("SELECT * FROM iplog")
	a = db.store_result().fetch_row(100000)
	db.close()
	return a