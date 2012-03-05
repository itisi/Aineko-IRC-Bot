def cmd_privmsg(bot,parts):
    if parts[0].split("!")[0].lower() == "chizu":
        name = "Hardcastle"
    else:
        name = "Bond"
    if "do you actually expect me" in parts[3].lower() or "do you expect me" in parts[3].lower():
        bot.send("KICK " + parts[2] + " " + parts[0] + " :No mister " + name + ", I expect you to *die*")
