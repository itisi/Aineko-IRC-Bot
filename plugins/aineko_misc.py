import time, random, traceback, os
def pm_chan(bot,parts):
	try:
		return " ".join(bot.registry["channels"][parts[3].split()[1].lower()]["nicks"])
	except:
		return "No such channel"
def pm_say(bot,parts):
	return parts[3].split(" ",1)[1]
def pm_whereis(bot,parts):
	"""Displays the location of the command specified"""
	print "lawl"
	try:
		if parts[3].split()[-1] in bot.registry["functions"]["pm"]:
			return " ".join(bot.registry["functions"]["pm"][parts[3].split()[-1]])
		else:
			return "No such command, or command is located in the bot core."
	except:
		traceback.print_exc()
def pm_modlist(bot,parts):
	try:
		all = os.listdir("./plugins")
		available = []
		for x in all:
			if len(x) >= 11 and x[:7] == "aineko_" and x[-3:] == ".py":
				available.append(x[7:-3])
		available.sort()
		retvar = []
		for x in available:
			if x in bot.registry["modules"]:
				retvar.append("\0033" + x + "\003")
			else:
				retvar.append("\0034" + x + "\003")
		return "Available modules: " + " ".join(retvar)
	except:
		traceback.print_exc()
def pm_version(bot,parts):
	if len(parts[3].split()) == 1: nick = parts[0]
	else: nick = parts[3].split()[1]

	if not nick.lower() in bot.registry["nicks"]:
		return "There is no " + nick + " connected to this network."
	elif not "version" in bot.registry["nicks"][nick.lower()]:
		return "Version for " + nick + " unknown."
	else:
		return nick + " is using client version: " + bot.registry["nicks"][nick.lower()]["version"]
def pm_test(bot,parts):
	return "Hello World"
def pm_spawn(bot,parts):
	if len(parts[3].split()) == 1:
		return "Requires at least 2 parameters (!spawn <nick>)"
	else:
		if not "child" in bot.registry:
			bot.registry["child"] = []
		nick = parts[3].split()[1]
		bot.registry["child"].append(nick)
		bot.servsend("NICK " + nick + " 1 " + str(int(time.time())) + " Mogget mogget MOGGET.MOGGET.MOGGET 0 :Aineko")
		bot.servsend(":" + nick + " JOIN " + parts[2])
def pm_despawn(bot,parts):
	if len(parts[3].split()) == 1:
		return "Requires at least 2 parameters (!despawn <nick>)"
	else:
		if not "child" in bot.registry:
			bot.registry["child"] = []
		nick = parts[3].split()[1]
		if not nick in bot.registry["child"]:
			return "No such child."
		else:
			bot.registry["child"].remove(nick)
			bot.servsend(":" + nick + " QUIT :Goodbye Cruel World.")
def pm_omnicide(bot,parts):
	if not "child" in bot.registry:
		return
	for nick in bot.registry["child"]:
		bot.servsend(":" + nick + " QUIT :If there's no one beside you when your soul embarks, then I'll follow you into the dark.")
	bot.registry["child"] = []
def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def pm_help(bot,parts):
	"""You're using it, nub."""
	if len(parts[3].split()) == 1:
		help = "Commands are: "
		commands = []
		for command in bot.registry["functions"]["pm"]:
			commands.append(command)
			commands.sort()
		chunked = list(chunks(commands,15))
		for chunk in chunked:
			help += ", ".join(chunk) + "\n"
		return help
	else:
		returnmessage = ""
		if parts[3].split()[1] in bot.registry["functions"]["pm"]:
			for module in bot.registry["functions"]["pm"][parts[3].split()[1]]:
				if getattr(bot.registry["modules"][module],"pm_" + parts[3].split()[1]).__doc__:
					returnmessage += getattr(bot.registry["modules"][module],"pm_" + parts[3].split()[1]).__doc__ + "\n"
				else: returnmessage += "No help for " + parts[3].split()[1] + "\n"
			return returnmessage
		else:
			return "No such command"
def pm_decide(bot,parts):
	"""Decide on one of the things in a comma separated list. !decide <item1>,<item2>,etc."""
	try:
		return "Decision: " + random.choice(parts[3].split(" ",1)[1].split(",")).strip()
	except:
		return "!decide <item1>,<item2>,etc."
def cmd_invite(bot,parts):
	if parts[2].lower() == bot.settings["nick"]:
		bot.send("JOIN " + parts[3][1:])