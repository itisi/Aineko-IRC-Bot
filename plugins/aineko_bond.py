def cmd_privmsg(bot,parts):
	if "do you actually expect me" in parts[3].lower() or "do you expect me" in parts[3].lower():
		bot.send(":aineko KICK " + parts[2] + " " + parts[0] + " :No mister Bond, I expect you to *die*")