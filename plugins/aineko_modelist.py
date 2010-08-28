def pm_mode(bot,parts):
	"""List modes for a channel or user. Usage: !mode <user/channel>"""
	if len(parts[3].split()) == 1:
		return "Usage: !mode <user/channel>"
	elif parts[3].split()[1][0] == "#" and parts[3].split()[1].lower() in bot.registry["channels"]:
		return "Modes for " + parts[3].split()[1] + ": " + "".join(bot.registry["channels"][parts[3].split()[1].lower()]["modes"].keys())
	elif parts[3].split()[1].lower() in bot.registry["nicks"]:
		return "Modes for " + parts[3].split()[1] + ": " + "".join(bot.registry["nicks"][parts[3].split()[1].lower()]["modes"].keys())
	else:
		return "User or channel does not exist."
def pm_identified(bot,parts):
	if "r" in bot.registry["nicks"][parts[0].lower()]["modes"]:
		return "You are identified with nickserv."
	else:
		return "You are not identified with nickserv."