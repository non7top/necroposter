#!/usr/bin/env python
# -*- coding: utf8 -*-


import sys
import base64
import re
import urllib
import urllib2
from StringIO import StringIO

from lxml import etree
from necrolib import utils
from necrolib import datadir
from cache import cache
import os

class cast():
	def __init__(self, wa_id):
                parser = etree.HTMLParser()
		self.id=wa_id
                self.homedir = datadir.user_data_dir("necroposter")
                cached = os.path.join (self.homedir, 'cache')
                self.cache = cache(cached)
		wa_addr = "http://world-art.ru/animation/animation_full_cast.php?id=%s" % self.id
                fname=self.id + '.cast.cache'
                body = self.cache.dw_html(wa_addr, fname)

                self.thepage = unicode( body,    "cp1251")
                self.tree = etree.parse(StringIO(self.thepage), parser)
                #self.thepage, self.tree = utils.dw_wapage(wa_addr)
                self.get_actors()

	def get_actors(self):
		self.actors=[]
		p = "//b[.  = '" + u'Роли озвучивали:' + "']"
		r = self.tree.xpath(p)[0].getparent().getparent().getparent().getparent()
                '''walk through all tr elements'''
		for q in r:
			#self.actors.append(q.text)
                        try:
                                rr = q.xpath("td[2]/a")
                                ac_name = rr[0].text
                                ac_id = utils.getnum(rr[0].get("href"))
                                ac_link = "http://world-art.ru/people.php?id=%s" % ac_id
                                rr = q.xpath("td[3]")
                                ac_role = rr[0].text[2:]
                                self.actors.append({'ac_name':ac_name,'ac_id':ac_id,'ac_role':ac_role,
                                    'ac_link':ac_link})
                        except IOError:
                                pass
                        except IndexError:
                                pass
                return self.actors
