import codecs
import re
import urllib2
from bs4 import BeautifulSoup
import feedparser

# Constants Definition
RSS_FEED = 'http://www.aaronsw.com/2002/feeds/pgessays.rss'
TEMPLATE = u'<html lang="en"><head><title>{0}</title></head><body>{1}</body></html>'
H1 = '<h1>{0}</h1>'

# Load and parses RSS feed
d = feedparser.parse(RSS_FEED)
print d.feed.title
print d.feed.description
	
for item in d.entries:
	print 'Processing...' + item.title + ' : ' + item.link
	
	try :		
		page = urllib2.urlopen(item.link)
		soup = BeautifulSoup(page)
		
		final = ''
		c = soup.find('td', width="455")
		
		if c is None:
			c = soup.find('td', width="375")
		
		if c is not None:	
			s = c.prettify()
			s = re.sub('<br>\s*\s<br>','</p><p>',s)
			s = re.sub('<font(\s*|.*|\s)>|</font>|<br>|</br>|<br/>|<td(\s*|.*|\s)>|</td>|</img>','',s)
			s = re.sub('<img(\s*|.*|\s)>\s*</p>',str.format(H1,item.title),s)
			s = re.sub('<p>\s*\s<b>','<h3>',s)
			s = re.sub('</b>\s*\s</p>','</h3>',s)
			s = TEMPLATE.format(item.title,s)
			
			soup = BeautifulSoup(s)
			month = soup.body.p
			month.name = 'h2'
			file_name = item.title+'.html'
			
			f = codecs.open(file_name, encoding='utf-8', mode='w+')
			f.write(soup.prettify())
			f.close()
		else:
			print 'Error in Template! ---------------------------'
	except:
		print "Unexpected error ---------------------------"
