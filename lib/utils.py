#!/usr/bin/env python
# -*- coding: utf8 -*-


import sys
import os
import base64
import re
import urllib
import urllib2
from StringIO import StringIO

from lxml import etree


'''return number from text'''
def getnum(txt):
    n = re.findall(r"\d+",txt)[0]
    return n
	
def dw_wapage(wa_addr):
    parser = etree.HTMLParser()
    
    req = urllib2.Request(wa_addr)

    try:
        handle = urllib2.urlopen(req)
    except IOError:
        print "ioerror"

    thepage = unicode( handle.read(),    "cp1251")
    tree = etree.parse(StringIO(thepage), parser)
    handle.close()
    return thepage, tree

