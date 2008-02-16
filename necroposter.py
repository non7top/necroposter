#!/usr/bin/env python
# -*- coding: utf8 -*-

import base64
import re
import urllib
import urllib2
from StringIO import StringIO

from lxml import etree


class necroposter():
	def __init__(self):
		self.parser = etree.HTMLParser()

	def dw_wapage(self,  wa_addr):
		print wa_addr
		req = urllib2.Request(wa_addr)
		
		try:
			handle = urllib2.urlopen(req)
		except IOError:
			print "ioerror"
		self.thepage = unicode( handle.read(),    "cp1251")
		self.tree = etree.parse(StringIO(self.thepage), self.parser)

	def get_title(self):
		r = self.tree.xpath('/html/body/center[2]/table[6]/tr/td/table/tr/td[5]/table/tr/td[3]/font/b')
		self.title = r[0].text[:-2].strip()
		return self.title

	def get_year(self):
		r = self.tree.xpath("/html/body/center[2]/table[6]/tr/td/table/tr/td[5]/table/tr/td[3]/a/font")
		#print etree.tostring(r[0])
		self.year = r[0].text.strip()
		return self.year
		
	def get_names(self):
		self.names=[]
		r = self.tree.xpath("/html/body/center[2]/table[6]/tr/td/table/tr/td[5]/table/tr/td[3]/br")
		for q in r:
			self.names.append(q.tail)
		return self.names
	
	def get_jenres(self):
		self.jenres=[]
		p = "//a[starts-with(@href, 'list.php?genre')]"
		r = self.tree.xpath(p)
		for q in r:
			self.jenres.append(q.text)
		return self.jenres
	
	def get_type(self):
		p="/html/body/center[2]/table[6]/tr/td/table/tr/td[5]/table/tr/td[3]/font[3]/b[3]"
		r = self.tree.xpath(p)
		self.type = r[0].tail[2:]
		return self.type

	def get_episodes(self):
		try:
			self.episodes=[]
			p = "//table[.  = '" + u'Эпизоды:' + "']"
			r = self.tree.xpath(p)[0].getnext().getnext()
			rr = r.xpath("tr/td[1]")
			self.episodes.append( rr[0].text )
			
			rrr = r.xpath('tr/td[1]/br')
			for q in rrr:
				self.episodes.append(q.tail)
			return self.episodes
		except:
			return 0

	#def get_
	def cat(self, xpath):
		r = self.tree.xpath(xpath)
		print etree.tostring(r[0])
	def lsch(self, xpath):
		r = self.tree.xpath(xpath)
		for c in r[0]:
			print c.tag
		pass

qqq=necroposter()
#qqq.dw_wapage("http://www.world-art.ru/animation/animation.php?id=2699")
qqq.dw_wapage("http://www.world-art.ru/animation/animation.php?id=82")
#print qqq.get_title()
#print qqq.get_year()
#print qqq.get_names()
#print qqq.get_jenres()
#print qqq.get_type()
print qqq.get_episodes()
#qqq.cat(p)
#qqq.lsch(p)
print "finish"
