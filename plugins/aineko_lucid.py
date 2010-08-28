import time,thread
def start(bot):
	if not "lucid" in bot.registry:
		bot.registry["lucid"] = 1
	thread.start_new_thread(lucidity,(bot,bot.registry["lucid"]))
def lucidity(bot,id):
	while "lucid" in bot.registry and bot.registry["lucid"] == id:
		bot.speak("#antischool","Are you dreaming?")
		bot.speak("#emo","Are you dreaming?")
		time.sleep(10800)
def stop(bot):
	bot.registry["lucid"] += 1