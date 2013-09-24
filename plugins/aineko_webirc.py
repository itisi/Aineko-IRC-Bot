from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import thread
import json
import time

protocol = None
bot = None
port = None

class webirc(LineReceiver):
    def __init__(self):
        pass

    def connectionMade(self):
        initvars = {
            'command': 'initvars',
            'channels': bot.registry['channels'],
            'nicks': {nick: {'channels':bot.registry['nicks'][nick]['channels']} for nick in bot.registry['nicks']}
        }
        print 'sending', initvars
        sendmessage(initvars)

    def connectionLost(self, reason):
        pass

    def lineReceived(self, line):
        try:
            line = json.loads(line)
        except ValueError:
            pass
        if 'command' in line:
            if hasattr(self, 'on_' + line['command']):
                getattr(self,'on_' + line['command'])(line)

    def on_privmsg(self, line):
        bot.speak(line['channel'], line['message'])
    def on_join(self, line):
        bot.send('JOIN ' + line['channel'])

class webircFactory(Factory):
    def __init__(self):
        pass

    def buildProtocol(self, addr):
        global protocol
        protocol = webirc()
        return protocol

def start(bot):
    global port
    globals()['bot'] = bot
    factory = webircFactory()
    port = reactor.listenTCP(9001, factory)
    thread.start_new_thread(reactor.run, (), {'installSignalHandlers': 0})
def stop(bot):
    global port, protocol
    port.stopListening()
    time.sleep(5)
    protocol.transport.loseConnection()
def cmd_privmsg(bot, parts):
    message = {
        'command': 'privmsg',
        'nick': parts[0][1:],
        'channel': parts[2],
        'message': parts[3][1:]
    }
    sendmessage(message)
def cmd_join(bot, parts):
    message = {
        'command': 'join',
        'nick': parts[0][1:],
        'channel': parts[2],
    }
    sendmessage(message)

def sendmessage(message):
    global protocol
    print 'sending'
    reactor.callFromThread(protocol.sendLine, json.dumps(message))