from core import bot
import thread
a = bot()
thread.start_new_thread(a.start,())
