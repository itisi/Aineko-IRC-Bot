import socket
import traceback
import proc
import os.path
from time import time
class bot:
    def __init__(self,configfile="aineko.conf"):
        if not os.path.isfile(configfile):
            exit("Error: There is no config file " + configfile)
        import ConfigParser
        config = ConfigParser.RawConfigParser()
        config.read(configfile)

        self.registry = {}
        self.cmdprefixes = ["pm", "cmd", "umu", "umd", "chu", "chd"]
        self.registry["nicks"] = {}
        self.registry["channels"] = {}
        self.registry["functions"] = {}
        self.registry["modules"] = {}
        self.registry["initialized"] = 0
        for prefix in self.cmdprefixes:
            self.registry["functions"][prefix] = {}
        self.connection = {'host':config.get('Server','hostname'),
                           'port':config.getint('Server','port'),
                           'password':config.get('Server','password')}
        self.settings = {'servername':config.get('Bot','servername'),
                         'description':config.get('Bot','serverdescription'),
                         'numeric':config.getint('Bot','servernumeric'),
                         'nick':config.get('Bot','defaultnick')}
        try:
            self.database = {'hostname':config.get('Database','hostname'),
                             'port':config.getint('Database','port'),
                             'user':config.get('Database','user'),
                             'password':config.get('Database','password'),
                             'database':config.get('Database','database')}
        except:
            self.database = 0
    def start(self):
        self.connection['socket'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection['socket'].connect((self.connection['host'],self.connection['port']))
        self.servsend("PASS :" + self.connection['password'])
        self.servsend("SERVER " + self.settings['servername'] + " " + str(self.settings['numeric']) + " :" + self.settings['description'])
        self.loop()
    def send(self,message,output=True,sendnick=0):
        if not sendnick:
            sendnick=self.settings["nick"]
        message = ":" + sendnick + " " + message.replace("\n","").replace("\r","")[:510]
        self.connection['socket'].send(message + "\r\n")
        print "SENDING: " + message
    def servsend(self,message,output=True):
        self.connection['socket'].send(message.replace("\n","").replace("\r","")[:510] + "\r\n")
        print "SENDING: " + message
    def loop(self):
        while 1:
            for line in self.getlines():
                self.handle(line)
        
    def getlines(self):
        message = ""
        runtime = 0
        while message.rfind("\n") == -1 or message.rfind("\n") != len(message) - 1:
            receive = self.connection['socket'].recv(1024)
            message += receive
            if not runtime:
                starttime = time()
            elif time() - starttime > 10:
                print "Server did something unexpected. Attempting to recover."
                break
        return message.splitlines()
    def speak(self, channel, message, nick=0):
        if not nick:
            nick=self.settings["nick"]
        self.send("PRIVMSG " + channel + " :" + message,sendnick=nick)
    def handle(self,line):
        print line
        parts = line.split(" ",3)
        while len(parts) <= 3:
            parts.append(self.settings["nick"])
        if parts[0] == "PING":
            self.servsend("PONG " + parts[1])
        if parts[1][0] == ":":
            parts[1] = parts[1][1:]
        if parts[2] and parts[2][0] == ":":
            parts[2] = parts[2][1:]
        if parts[0] == "ERROR":
            exit("Server terminated connection.")
        elif parts[1] == "PRIVMSG" and parts[3] == ":.reload":
            try:
                reload(proc)
                proc.refresh(self)
                reload(proc)
                self.speak(parts[2],"Reload Successful")    
            except:
                self.speak(parts[2],"Reload Failed")
                traceback.print_exc()
                
        else:
            try:
                proc.handle(self,parts) #bot line
            except:
                traceback.print_exc()