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
		wa_addr = "http://world-art.ru/animation/animation_full_cast.php?id=%s" % self.id
        
                self.thepage, self.tree = utils.dw_wapage(wa_addr)
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
