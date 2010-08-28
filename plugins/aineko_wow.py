import traceback
def cmd_privmsg(bot,parts):
	if parts[2].lower() == "#wow":
		a = parts[3][1:]
		import urllib,amara
		if a.find("[") >= 0 and a.find("]") >= a.find("["):
			item = a[a.find("[") + 1:a.find("]")]
			params = urllib.urlencode({'item': item})
			xml = amara.parse("http://www.wowhead.com/?%s&xml" % params)
			try:
				if xml.wowhead.item.quality == "Epic":
					return "\0036[%s]\003 (%s %s): %s" % (xml.wowhead.item.name, xml.wowhead.item.level, xml.wowhead.item.subclass, xml.wowhead.item.link)
				elif xml.wowhead.item.quality == "Rare":
					return "\00312[%s]\003 (%s %s): %s" % (xml.wowhead.item.name, xml.wowhead.item.level, xml.wowhead.item.subclass, xml.wowhead.item.link)
				elif xml.wowhead.item.quality == "Uncommon":
					return "\0039[%s]\003 (%s %s): %s" % (xml.wowhead.item.name, xml.wowhead.item.level, xml.wowhead.item.subclass, xml.wowhead.item.link)
				elif xml.wowhead.item.quality == "Common":
					return "\00316[%s]\003 (%s %s): %s" % (xml.wowhead.item.name, xml.wowhead.item.level, xml.wowhead.item.subclass, xml.wowhead.item.link)
				elif xml.wowhead.item.quality == "Poor":
					return "\00314[%s]\003 (%s %s): %s" % (xml.wowhead.item.name, xml.wowhead.item.level, xml.wowhead.item.subclass, xml.wowhead.item.link)
				elif xml.wowhead.item.quality == "Legendary":
					return "\0034[%s]\003 (%s %s): %s" % (xml.wowhead.item.name, xml.wowhead.item.level, xml.wowhead.item.subclass, xml.wowhead.item.link)
				elif xml.wowhead.item.quality == "Heirloom":
					return "\0037[%s]\003 (%s %s): %s" % (xml.wowhead.item.name, xml.wowhead.item.level, xml.wowhead.item.subclass, xml.wowhead.item.link)
			except:
				pass