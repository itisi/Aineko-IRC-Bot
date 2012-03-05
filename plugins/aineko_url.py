import filemagic
import thread
import lxml.html
import urllib
import time
def cmd_privmsg(bot,parts):
    if "http://" in parts[3]:
        thread.start_new_thread(procurl,(bot,parts,"http://"))
    elif "https://" in parts[3]:
        thread.start_new_thread(procurl,(bot,parts,"https://"))

class AppURLopener(urllib.FancyURLopener):
    version = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.237 Safari/534.10"

urllib._urlopener = AppURLopener()
def procurl(bot,parts,prot):
    urllib._urlopener = AppURLopener()
    urlstring = parts[3][parts[3].find(prot):].split()[0]
    if urlstring[-1] == '\001':
        urlstring = urlstring[:-1]
    url = urllib.urlopen(urlstring)

    type = url.info().gettype()
    if type in ["image/jpeg", "image/png"]:
        thread.start_new_thread(getimage, (bot, parts, url, type))
    ret = "Type: " + type
    if type == "text/html":
        try:
            data = url.read()
            t = lxml.html.document_fromstring(data)
            title = t.find(".//title").text.encode("utf-8","replace")
            
        except:
            title = "untitled"
        ret += " Title: " + title
    bot.speak(parts[2],ret)
def getimage(bot, parts, url, type):
    ctime = str(int(time.time()))
    ftype = {"image/jpeg":".jpg","image/png":".png"}[type]
    file = "/home/bots/aineko/images/" + ctime + ftype
    a = open(file,"w")
    a.write(url.read())
    mime = filemagic.Magic(mime=True)
    atype = mime.from_file(file)
    if atype == "image/gif":
        bot.speak(parts[2],"\0034Warning: Image was transfered as %s but appears to be image/gif.  Probable trolling attempt.\003" % type)
    
