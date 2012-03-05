import time
def cmd_privmsg(bot,parts):
	if "madness" in parts[3].lower():
		return """            MADNESS?!
          o   THIS IS SPARTA!
         /|__       
          |          >--/o  
    [][][][]                     [][][][]
    [][][][]                     [][][][]
    [][][][]                     [][][][]"""
def cmd_privmsg(bot,parts):
    if "trollolol" in parts[3] or "trololol" in parts[3]:
        if not "trollolol" in store:
            go = True
            store["trollolol"] = time.time()
        else:
            if time.time() - store["trollolol"] >= 3600:
                go = True
                store["trollolol"] = time.time()
        if go:
            trollface(bot,parts)
def trollface(bot,parts):
    a = open("trollface.txt").readlines()
    for line in a:
        bot.speak(parts[2],line)