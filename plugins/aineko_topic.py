def pm_t(bot,parts):
	"""!t add <text>, !t rep <int> <text>, !t del <int>"""
	from string import strip
	channel = parts[2]
	if not "topic" in bot.registry:
		bot.registry["topic"] = {}
	oldtopic = bot.registry["channels"][parts[2].lower()]["topic"]
	modification = parts[3].split(" ",2)
	if len(modification) == 1:
		bot.speak(channel,"Options are add, del, and rep")
	else:
		if modification[1] == "add":
			if oldtopic == "":
				topicparts = []
			else:
				topicparts = map(strip, oldtopic.split("|"))
			if len(modification) == 2:
				bot.speak(channel,"Nothing to add. :\\")
			else:
				topicparts.append(modification[2])
				bot.registry["channels"][parts[2].lower()]["topic"] = " | ".join(topicparts)
				bot.send("TOPIC " + channel + " :" + bot.registry["channels"][parts[2].lower()]["topic"])
		elif modification[1] == "push":
			if oldtopic == "":
				topicparts = []
			else:
				topicparts = map(strip, oldtopic.split("|"))
			if len(modification) == 2:
				botbot.speak(channel,"Nothing to add. :\\")
			else:
				topicparts.insert(0,modification[2])
				bot.registry["channels"][parts[2].lower()]["topic"] = " | ".join(topicparts)
				bot.send("TOPIC " + channel + " :" + bot.registry["channels"][parts[2].lower()]["topic"])
		elif modification[1] == "del":
			topicparts = map(strip, oldtopic.split("|"))
			if len(modification) == 2:
				bot.speak(channel,"Nothing to delete. :\\")
			else:
				try:
					topicpart = int(modification[2])
					if topicpart > 0:
						topicpart -= 1
					elif topicpart == 0:
						topicpart = 'x'
						bot.speak(channel,"Positive integer to count from beginning. Negative to count from end.")
					else:
						pass
					if topicpart != 'x':
						del(topicparts[topicpart])
						bot.registry["channels"][parts[2].lower()]["topic"] = " | ".join(topicparts)
						bot.send("TOPIC " + channel + " :" + bot.registry["channels"][parts[2].lower()]["topic"])
				except:
					traceback.print_exc()
					bot.speak(channel,"Parameter was not an integer, or the integer was out of range.")
		elif modification[1] == "rep":
			topicparts = map(strip, oldtopic.split("|"))
			if len(modification) == 2:
				bot.speak(channel,"Nothing to replace. :\\")
			else:
				try:
					modparts = modification[2].split(" ",1)
					topicpart = int(modparts[0])
					if topicpart > 0:
						topicpart -= 1
					elif topicpart == 0:
						topicpart = 'x'
						bot.speak(channel,"Positive integer to count from beginning. Negative to count from end.")
					else:
						pass
					if topicpart != 'x':
						topicparts[topicpart] = modparts[1]
						bot.registry["channels"][parts[2].lower()]["topic"] = " | ".join(topicparts)
						bot.send("TOPIC " + channel + " :" + bot.registry["channels"][parts[2].lower()]["topic"])
				except:
					traceback.print_exc()
					bot.speak(channel,"Parameter was not an integer, integer was out of range, or no replacement was specified.")