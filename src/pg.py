#!/usr/bin/python
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

__author__ = "Gilbert Corrales (gcorrales@gmail.com)"
__copyright__ = "Copyright (C) 2012 Gilbert Corrales"
__license__ = "LGPL 3.0"
__version__ = "0.3"

import codecs
import re
import urllib2
from bs4 import BeautifulSoup
import feedparser

# Constants Definition
RSS_FEED = 'http://www.aaronsw.com/2002/feeds/pgessays.rss'
TEMPLATE = u'<html lang="en"><head><title>{0}</title></head><body>{1}<p>This essay was originally published at <a href="{2}?utm_source=pgebook">paulgraham.com</a><p></body></html>'
H1 = '<h1>{0}</h1>'

# Load and parses RSS feed
d = feedparser.parse(RSS_FEED)
print d.feed.title
print d.feed.description

for idx, item in enumerate(d.entries):
	print 'Processing...' + item.title + ' : ' + item.link
	
	try :		
		page = urllib2.urlopen(item.link)
		soup = BeautifulSoup(page)
		
		final = ''
		c = soup.find('td', width="455")
		
		if c is None:
			c = soup.find('td', width="375")

		cc = soup.findAll(cellspacing="0",width="100%")
		[comment.extract() for comment in cc]

		if c is not None:
			s = c.prettify()
			s = re.sub('<br>\s*\s<br>','</p><p>',s)
			s = re.sub('<font(\s*|.*|\s)>|</font>|<br>|</br>|<br/>|<td(\s*|.*|\s)>|</td>|</img>','',s)
			s = re.sub('<img(\s*|.*|\s)>\s*</p>',str.format(H1,item.title),s)
			s = re.sub('<p>\s*\s<b>','<h3>',s)
			s = re.sub('</b>\s*\s</p>','</h3>',s)
			s = TEMPLATE.format(item.title,s,item.link)
			
			soup = BeautifulSoup(s)
			month = soup.body.p
			month.name = 'h2'			
			file_name = str(idx)+' - '+item.title+'.html'
			
			f = codecs.open(file_name, encoding='utf-8', mode='w+')
			f.write(soup.prettify())
			f.close()
		else:
			print 'Error in Template! ---------------------------'
	except:
		print "Unexpected error ---------------------------"
