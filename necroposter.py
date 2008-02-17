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
		wa_addr = "http://www.world-art.ru/animation/animation.php?id=%s" %wa_addr
		print wa_addr
		req = urllib2.Request(wa_addr)
		
		try:
			handle = urllib2.urlopen(req)
		except IOError:
			print "ioerror"
		self.thepage = unicode( handle.read(),    "cp1251")
		self.tree = etree.parse(StringIO(self.thepage), self.parser)
		handle.close()

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
			print ">> Single episode"
			return 0

	def get_series(self):
		try:
			self.series = []
			p = "//table[.  = '" + u'В каком порядке лучше смотреть эту серию:' + "']"
			r = self.tree.xpath(p)[0].getnext().getnext()
			
			'''прогоняем по списку серий'''
			for q in r:
				rr = q.xpath('td[3]/a')
				self.series.append(rr[0].text + rr[0].tail)
			return self.series
		except:
			print ">> Single serie"
			return 0

	def get_imglink(self):
		p="/html/body/center[2]/table[6]/tr/td/table/tr/td[5]/table/tr/td/img"
		r = self.tree.xpath(p)
		link='http://www.world-art.ru/animation/' + r[0].get("src")
		fname=r[0].get("alt") + '.jpg'
		self.imglink={'link':link,  'fname':fname}
		return self.imglink

	def dw_img(self, imglink):
		fname=imglink['fname']
		link=imglink['link']
		outputFile = open(fname,"wb")
		
		req = urllib2.Request(link)
		try:
			handle = urllib2.urlopen(req)
		except IOError:
			print "ioerror"
		
		data = handle.read()
		outputFile.write(data)
		outputFile.close()
		handle.close()
	
	def init_data(self):
		self.get_title()
		self.get_year()
		self.get_names()
		self.get_jenres()
		self.get_type()
		self.get_episodes()
		self.get_series()
		il=self.get_imglink()
		self.dw_img(il)
		print ">>Init done"

	def gen_bbcode(self):
		pass
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
qqq.dw_wapage("82")
qqq.init_data()
print "finish"
