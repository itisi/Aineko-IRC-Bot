import urllib, httplib, sys

def pm_calc(bot,parts):
	"""Google calculator"""
	string = parts[3].split(" ",1)[1]
	query=urllib.urlencode({'q':string})

	start='<h2 class=r style="font-size:138%"><b>'
	end='</b>'

	google=httplib.HTTPConnection("www.google.com")
	google.request("GET","/search?"+query)
	search=google.getresponse()
	data=search.read()

	if data.find(start)==-1: return "Invalid calculation."
	else:
		begin=data.index(start)
		result=data[begin+len(start):begin+data[begin:].index(end)]
		result = result.replace("<font size=-2> </font>",",").replace(" &#215; 10<sup>","E").replace("</sup>","").replace("\xa0",",")
		return result
pm_convert = pm_calc