#!/usr/bin/env python
# -*- coding: utf8 -*-


############################################################################
#    Copyright (C) 2007 by non7top   #
#    non7top@gmail.com   #
#                                                                          #
#    This program is free software; you can redistribute it and#or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation;  version 2 of the License and all later version.                                   #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software Foundation, Inc.,                                       #
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################

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

def get_urls(data):
    # Pattern for fully-qualified URLs:
    url_pattern = re.compile('''["']http://[^+]*?['"]''')

    # build list of all URLs found in standard input
    #s = sys.stdin.read()
    all = url_pattern.findall(data)

    return all
    # output all the URLs
    #for i in all:
    #        print i.strip('"').strip("'")

def get_urls_meta(data):
    # Pattern for fully-qualified URLs:
    url_pattern = re.compile('''=http://[^+]*?[']''')

    # build list of all URLs found in standard input
    #s = sys.stdin.read()
    all = url_pattern.findall(data)
    
    # output all the URLs
    k = all[0].strip('=').strip("'")
    return k
