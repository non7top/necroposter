#!/usr/bin/env python
# -*- coding: utf8 -*-


import sys
import base64
import re
import urllib
import urllib2
from StringIO import StringIO

from lxml import etree
from lib import utils

class cast():
	def __init__(self, wa_id):
		self.id=wa_id
		self.wa_addr = "http://world-art.ru/animation/animation_full_cast.php?id=%s" % self.id
        
                self.thepage, self.tree = utils.dw_wapage(wa_addr)

	def get_jenres(self):
		self.jenres=[]
		p = "//a[starts-with(@href, 'list.php?genre')]"
		r = self.tree.xpath(p)
		for q in r:
			self.jenres.append(q.text)
		return self.jenres
	
	def get_series(self):
		try:
			self.series = []
			p = "//table[.  = '" + u'В каком порядке лучше смотреть эту серию:' + "']"
			r = self.tree.xpath(p)[0].getnext().getnext()
			
			'''прогоняем по списку серий'''
			for q in r:
				rr = q.xpath('td[3]/a')
				self.series.append(rr[0].text + rr[0].tail)
			self.has_s = 1
			return self.series
		except:
			print ">> Single serie"
			self.has_s = 0
			return 0
        
        def get_desc(self):
                try:
                        p = "//table[.  = '" + u'Краткое содержание:' + "']"
                        r = self.tree.xpath(p)[0].getnext().getnext()
                        rr=r.xpath('tr/td/p')
                        self.desc=rr[0].text
                except:
                        self.desc = 0
                        print ">>>> No desc"



        
        '''return number from text'''
        def getnum(self, txt):
                n = re.findall(r"\d+",txt)[0]
                return n
	
	def chkdirs(self):
		self.mkdir('studio')
		self.mkdir('cover')

	def mkdir(self, dir):
                if not os.path.isdir(dir):
			os.mkdir(dir)
		
	def cat(self, r):
		print etree.tostring(r[0])

	def lsch(self, xpath):
		r = self.tree.xpath(xpath)
		for c in r[0]:
			print c.tag
		pass
	

def main(n):
	if len(n) == 0:
		print "Give pagenumber or full link as an argument"
		sys.exit(1)
	else:
		np=necroposter()
		np.dw_wapage(n[0])
		#print np.get_episodes()
		np.init_data()
		np.gen_bbcode()
		
if __name__ == "__main__":
    main(sys.argv[1:])
