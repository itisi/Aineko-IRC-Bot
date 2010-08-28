import time, traceback, _mysql
def refresh(bot):
    for module in bot.registry["modules"]:
        reload(bot.registry["modules"][module])
def handle(bot,parts):
    if "cmd_" + parts[1] in globals():
        try:
            globals()["cmd_" + parts[1]](bot,parts)
        except:
            traceback.print_exc()
    if "serv_" + parts[0] in globals():
        try:
            globals()["serv_" + parts[0]](bot,parts)
        except:
            traceback.print_exc()
    elif parts[1].lower() in bot.registry["functions"]["cmd"]:
        for module in bot.registry["functions"]["cmd"][parts[1].lower()]:
            try:
                response = getattr(bot.registry["modules"][module],"cmd_" + parts[1].lower())(bot,parts)
            except:
                response = None
            if response:
                if parts[2][0] == '#':
                    for line in response.split('\n'):
                        bot.speak(parts[2],line)
                else:
                    for line in response.split('\n'):
                        bot.speak(parts[0],line)
def cmd_PRIVMSG(bot,parts):
    parts[0] = parts[0][1:]
    try:
        if self.database:
            db = _mysql.connect(host=self.database["hostname"], port=self.database["port"], user=self.database["user"], passwd=self.database["password"], db=self.database["database"])
            db.query("INSERT INTO privmsg (time,nick,channel,message) VALUES ('" + str(int(time.time())) + "','" + _mysql.escape_string(parts[0].split('!')[0]) + "', '" + _mysql.escape_string(parts[2]) + "', '" + _mysql.escape_string(parts[3][1:]) + "')")
            db.close()
    except:
        pass
    if parts[2][0] != '#':
        chan = parts[0]
    else:
        chan = parts[2]
    if len(parts[3]) > 3 and parts[3][1] == '!' and "pm_" + parts[3][2:].split()[0] in globals():
        try:
            retmessage = globals()["pm_" + parts[3][2:].split()[0]](bot,parts)
        except:
            retmessage = None
        if retmessage:
            for line in retmessage.split('\n'):
                bot.speak(chan,line)
    if len(parts[3]) > 3 and parts[3][1] == '!' and parts[3].split()[0][2:] in bot.registry["functions"]["pm"]:
        for module in bot.registry["functions"]["pm"][parts[3].split()[0][2:]]:
            try:
                retmessage = getattr(bot.registry["modules"][module],"pm_" + parts[3].split()[0][2:])(bot,parts)
            except:
                traceback.print_exc()
                retmessage = None
            if retmessage:
                for line in retmessage.split('\n'):
                    bot.speak(chan,line)
def modload(bot,module):
    import os
    if module in bot.registry["modules"]:
        return ["Module already loaded."]
    elif not "aineko_" + module + ".py" in os.listdir("./plugins"):
        return ["Module does not exist"]
    else:
        retvar = []
        try:
            plugins = __import__("plugins.aineko_" + module)
            bot.registry["modules"][module] = getattr(plugins,"aineko_" + module)
            if not "store_" + module in bot.registry: # Assigns a "store" variable in a module's namespace that can be used to store information the persists after the module is unloaded.
                bot.registry["store_" + module] = {}
            bot.registry["modules"][module].store = bot.registry["store_" + module]
            reload(bot.registry["modules"][module])
            for function in dir(bot.registry["modules"][module]):
                if "_" in function and function.split("_")[0] in bot.cmdprefixes and len(function) > len(function.split("_")[0]) + 1:
                    prefix = function.split("_")[0]
                    if not function[len(prefix) + 1:] in bot.registry["functions"][prefix]:
                        bot.registry["functions"][prefix][function[len(prefix) + 1:]] = []
                    bot.registry["functions"][prefix][function[len(prefix) + 1:]].append(module)
            if "start" in dir(bot.registry["modules"][module]):
                try:
                    getattr(bot.registry["modules"][module],"start")(bot)
                except:
                    traceback.print_exc()
                    retvar.append("Functions loaded, but constructor failed to execute. Possible registry errors.")
        except:
            traceback.print_exc()
            retvar.append("Failed to load module. Probable syntax error.")
        return retvar

def modunload(bot,module):
    if not module in bot.registry["modules"]:
        return ["Module does not exist"]
    else:
        retvar = []
        try:
            for function in dir(bot.registry["modules"][module]):
                if "_" in function and function.split("_")[0] in bot.cmdprefixes:
                    prefix = function.split("_")[0]
                    if len(function) > len(prefix) + 1:
                        bot.registry["functions"][prefix][function[len(prefix) + 1:]].remove(module)
                        if not len(bot.registry["functions"][prefix][function[len(prefix) + 1:]]):
                            del(bot.registry["functions"][prefix][function[len(prefix) + 1:]])
        except:
            retvar.append("Error removing all functions from registry. Possible ghosts.")
            traceback.print_exc()
        if "stop" in dir(bot.registry["modules"][module]):
            try:
                getattr(bot.registry["modules"][module],"stop")(bot)
            except:
                del(bot.registry["modules"][module])
                traceback.print_exc()
                retvar.append("Error processing deconstructor. Module removed, but there could be registry errors.")
        del(bot.registry["modules"][module])
        return retvar
def pm_modload(bot,parts):
    status = modload(bot,parts[3].split()[1])
    if not status:
        return "Module loaded successfully."
    else:
        return "\n".join(status)
def pm_modunload(bot,parts):
    status = modunload(bot,parts[3].split()[1])
    if not len(status):
        return "Module unloaded successfully."
    else:
        return "\n".join(status)
def pm_modreload(bot,parts):
    status = modunload(bot,parts[3].split()[1]) + modload(bot,parts[3].split()[1])
    if not len(status):
        return "Module reloaded successfully."
    else:
        return "\n".join(status)
def serv_NICK(bot,parts):
    parts[1] = parts[1].lower()
    bot.registry["nicks"][parts[1]] = {}
    bot.registry["nicks"][parts[1]]["time"] = parts[3].split()[0]
    bot.registry["nicks"][parts[1]]["user"] = parts[3].split()[1]
    bot.registry["nicks"][parts[1]]["host"] = parts[3].split()[2]
    bot.registry["nicks"][parts[1]]["server"] = parts[3].split()[3]
    bot.registry["nicks"][parts[1]]["service"] = parts[3].split()[4]
    bot.registry["nicks"][parts[1]]["name"] = parts[3].split(" ",5)[5][1:]
    bot.registry["nicks"][parts[1]]["channels"] = []
    bot.registry["nicks"][parts[1]]["modes"] = {}
    if bot.registry["initialized"]:
        if "userinit" in bot.registry["functions"]["cmd"]:
            for module in bot.registry["functions"]["cmd"]["userinit"]:
                getattr(bot.registry["modules"][module],"cmd_userinit")(bot,parts)
        bot.speak(parts[1],"\001VERSION\001")
def serv_TOPIC(bot,parts):
    parts[1] = parts[1].lower()
    if not parts[1] in bot.registry["channels"]:
        bot.registry["channels"][parts[1]] = {}
    bot.registry["channels"][parts[1]]["topic"] = parts[3].split(" ",1)[1][1:]
def serv_NETINFO(bot,parts):
    bot.registry["initialized"] = 1
    initialize(bot)

def initialize(bot):
    bot.send("NICK " + bot.settings["nick"] + " 1 " + "0" + " " + bot.settings["nick"] + " \0037*\003 " + bot.settings["servername"] + " 0 :" + bot.settings["nick"])
    bot.send(":" + bot.settings["nick"] + " v " + bot.settings["nick"] + " +Wqp")
    for channel in bot.registry["channels"]:
        bot.send(":" + bot.settings["nick"] + " JOIN " + channel)
        bot.send(":" + bot.settings["nick"] + " MODE " + channel + " +v " + bot.settings["nick"])
    for nick in bot.registry["nicks"]:
        bot.speak(nick,"\001VERSION\001")
def cmd_KILL(bot,parts):
    time.sleep(10)
    if parts[2].lower() == bot.settings["nick"].lower():
        initialize(bot)
def cmd_TOPIC(bot,parts):
    bot.registry["channels"][parts[2]]["topic"] = parts[3].split(" ",2)[2][1:]
def cmd_NICK(bot,parts):
    if parts[0][1:].lower() == parts[2].lower():
        pass
    else:
        for channel in bot.registry["nicks"][parts[0][1:].lower()]["channels"]:
            try:
                print channel,parts[0][1:].lower()
                bot.registry["channels"][channel]["nicks"].remove(parts[0][1:].lower())
            except:
                traceback.print_exc()
        bot.registry["channels"][channel]["nicks"].append(parts[2].lower())
        bot.registry["nicks"][parts[2].lower()] = bot.registry["nicks"][parts[0][1:].lower()]
        del(bot.registry["nicks"][parts[0][1:].lower()])
def cmd_QUIT(bot,parts):
    for channel in bot.registry["nicks"][parts[0][1:].lower()]["channels"]:
        try:
            bot.registry["channels"][channel]["nicks"].remove(parts[0][1:].lower())
            if not len(bot.registry["channels"][channel]["nicks"]):
                bot.send(":Aineko PART " + channel + " :Channel disbanding.")
                del(bot.registry["channels"][channel.lower()])
                bot.speak("#botfucking",channel + " is now empty.")
        except:
            traceback.print_exc()
    del(bot.registry["nicks"][parts[0][1:].lower()])
def cmd_PART(bot,parts):
    if parts[2].lower() in bot.registry["channels"] and parts[0][1:].lower() in bot.registry["channels"][parts[2].lower()]["nicks"]:
        bot.registry["channels"][parts[2].lower()]["nicks"].remove(parts[0][1:].lower())
        if not len(bot.registry["channels"][parts[2].lower()]["nicks"]):
            bot.send(":Aineko PART " + parts[2] + " :Channel disbanding.")
            del(bot.registry["channels"][parts[2].lower()])
            bot.speak("#botfucking",parts[2] + " is now empty.")
def cmd_KICK(bot,parts):
    bot.registry["channels"][parts[2]]["nicks"].remove(parts[3].split()[0].lower())
    if not len(bot.registry["channels"][parts[2].lower()]["nicks"]):
        bot.send(":Aineko PART " + parts[2] + " :Channel disbanding.")
        del(bot.registry["channels"][parts[2].lower()])
        bot.speak("#botfucking",parts[2] + " is now empty.")
def cmd_NOTICE(bot,parts):
    if len(parts[3].split()) > 5 and parts[3].split()[5] == "/whois":
        bot.speak("#botfucking",parts[3].split()[1] + " did a whois on me.")
        bot.speak(parts[3].split()[1],"RAWR")
    elif len(parts[3].split()) > 9 and parts[3].split()[5] == "kick":
        if parts[3].split()[9] != "#botfucking":
            bot.speak("#botfucking",parts[3].split()[2] + " tried to kick me from " + parts[3].split()[9] + ".")
        bot.speak(parts[3].split()[9],parts[3].split()[2] + " tried to kick me from this channel. " + parts[3][parts[3].find("("):])
    elif parts[3][1:9].lower() == '\001version':
        bot.registry["nicks"][parts[0][1:].lower()]["version"] = parts[3][10:-1]
def cmd_JOIN(bot,parts):
    parts[2] = parts[2].lower()
    channels = parts[2].split(",")
    for channel in channels:
        bot.registry["nicks"][parts[0][1:].lower()]["channels"].append(channel)
        if not channel in bot.registry["channels"]:
            bot.registry["channels"][channel] = {}
            bot.registry["channels"][channel]["topic"] = ""
            bot.registry["channels"][channel]["nicks"] = []
            bot.registry["channels"][channel]["modes"] = {}
            if bot.registry["initialized"]:
                bot.send(":Aineko JOIN " + channel)
                bot.send(":Aineko MODE " + channel + " +v Aineko")
                bot.speak("#botfucking",parts[2] + " has been created. (" + parts[0][1:] + ")")
        if not parts[0][1:].lower() in bot.registry["channels"][channel]["nicks"]:
            bot.registry["channels"][channel]["nicks"].append(parts[0][1:].lower())
def cmd_MODE(bot,parts):
    mode = parts[3].split()[0]
    vars = parts[3].split()[1:]
    set = "+"
    changes = []
    var = 0
    if parts[2][0] == "#":
        spec = "abefhIjklLoqv"
        exclude = "abeIoqv"
        for x in mode:
            if x == ":":
                pass
            elif x == "+":
                set = "+"
            elif x == "-":
                set = "-"
            else:
                if x in spec and not (x == "l" and set == "-"):
                    changes.append([set,x,vars[var]])
                    var += 1
                else:
                    changes.append([set,x,1])
        for change in changes:
            if change[0] == "+":
                if change[1] in bot.registry["functions"]["chu"]:
                    for module in bot.registry["functions"]["chu"][change[1]]:
                        try:
                            retmessage = getattr(bot.registry["modules"][module],"chu_" + change[1])(bot,parts)
                        except:
                            retmessage = None
                    if retmessage:
                        for line in retmessage.split('\n'):
                            bot.speak(parts[2],line)
                if change[1] not in exclude:
                    bot.registry["channels"][parts[2].lower()]["modes"][change[1]] = change[2]
            else:
                if change[1] in bot.registry["functions"]["chd"]:
                    for module in bot.registry["functions"]["chd"][change[1]]:
                        try:
                            retmessage = getattr(bot.registry["modules"][module],"chd_" + change[1])(bot,parts)
                        except:
                            retmessage = None
                    if retmessage:
                        for line in retmessage.split('\n'):
                            bot.speak(parts[2],line)
                if change[1] not in exclude:
                    if change[1] in bot.registry["channels"][parts[2].lower()]["modes"]:
                        del(bot.registry["channels"][parts[2].lower()]["modes"][change[1]])
    else:
        for x in mode:
            if x == ":":
                pass
            elif x == "+":
                set = "+"
            elif x == "-":
                set = "-"
            elif x == "d":
                if len(vars):
                    pass
                else:
                    changes.append([set,x,1])
            else:
                changes.append([set,x,1])
        for change in changes:
            if change[0] == "+":
                if change[1] in bot.registry["functions"]["umu"]:
                    for module in bot.registry["functions"]["umu"][change[1]]:
                        try:
                            retmessage = getattr(bot.registry["modules"][module],"umu_" + change[1])(bot,parts)
                        except:
                            retmessage = None
                    if retmessage:
                        for line in retmessage.split('\n'):
                            bot.speak(parts[2],line)
                bot.registry["nicks"][parts[2].lower()]["modes"][change[1]] = change[2]
            else:
                if change[1] in bot.registry["functions"]["umd"]:
                    for module in bot.registry["functions"]["umd"][change[1]]:
                        try:
                            retmessage = getattr(bot.registry["modules"][module],"umd_" + change[1])(bot,parts)
                        except:
                            retmessage = None
                    if retmessage:
                        for line in retmessage.split('\n'):
                            bot.speak(parts[2],line)
                if change[1] in bot.registry["nicks"][parts[2].lower()]["modes"]:
                    del(bot.registry["nicks"][parts[2].lower()]["modes"][change[1]])
    for change in changes:
        print change
cmd_SVSMODE = cmd_MODE
cmd_SVS2MODE = cmd_MODE