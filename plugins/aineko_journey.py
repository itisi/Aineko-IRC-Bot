import time
import thread
def cnot(message,bot,channel,delay=1):
    time.sleep(delay)
    bot.send("NOTICE " + channel + " :" + message)
def pm_journey(bot,parts):
    thread.start_new_thread(journey,(bot,parts[2]))
def journey(bot, channel):
    cnot("Just",bot,channel,0)
    cnot("      a",bot,channel,.1)
    cnot("         small",bot,channel,.3)
    cnot("             town",bot,channel,.3)
    cnot("                  girl...",bot,channel,.3)
    cnot("Livin'",bot,channel,1)
    cnot("      in",bot,channel,.2)
    cnot("         a",bot,channel,.3)
    cnot("             lonely",bot,channel,.3)
    cnot("                  world...",bot,channel,.7)
    cnot("She",bot,channel,1)
    cnot("      took ",bot,channel,.3)
    cnot("         the",bot,channel,.3)
    cnot("             midnight",bot,channel,.3)
    cnot("                  train",bot,channel,.4)
    cnot("                     going",bot,channel,.3)
    cnot("                       an-",bot,channel,.6)
    cnot("                          y-",bot,channel,.3)
    cnot("                            where",bot,channel,.2)