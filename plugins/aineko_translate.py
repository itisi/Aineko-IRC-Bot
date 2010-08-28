import urllib
def pm_tr(bot,parts):
	"""arabic":"ar", "bulgarian":"bg", "chinese":"zh-CN", "croatian":"hr", "czech":"cs", "danish":"da", "dutch":"nl", "english":"en", "finnish":"fi", "french":"fr", "german":"de", "greek":"el", "hindi":"hi", "italian":"it", "japanese":"ja", "korean":"ko", "norwegian":"no", "polish":"pl", "portugese":"pt", "romanian":"ro", "russian":"ru", "spanish":"es", "swedish":"sv\""""
	lang={ "arabic":"ar", "bulgarian":"bg", "chinese":"zh-CN", "croatian":"hr", "czech":"cs", "danish":"da", "dutch":"nl", "english":"en", "finnish":"fi", "french":"fr", "german":"de", "greek":"el", "hindi":"hi", "italian":"it", "japanese":"ja", "korean":"ko", "norwegian":"no", "polish":"pl", "portugese":"pt", "romanian":"ro", "russian":"ru", "spanish":"es", "swedish":"sv" }
	if parts[3].split()[1].lower() in lang:
		start = lang[parts[3].split()[1].lower()]
	else:
		start = parts[3].split()[1].lower()
	if parts[3].split()[2].lower() in lang:
		end = lang[parts[3].split()[2].lower()]
	else:
		end = parts[3].split()[2].lower()	
	params = urllib.urlencode({'v': "1.0", 'q': parts[3].split(" ",3)[3], 'langpair': start + "|" + end})
	f = urllib.urlopen("http://ajax.googleapis.com/ajax/services/language/translate?%s" % params)
	a = f.read()
	print a
	a = a[a.find("translatedText") +17:]
	a = a[:a.find("\"")]
	return a
pm_translate = pm_tr