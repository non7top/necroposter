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
		pass


	def addlink(self, url):
	
		theurl = 'http://litops.hq.aaanet.ru/cts_support/cts_s_jinn'
		# if you want to run this example you'll need to supply
		# a protected page with your username and password
		#url='http://brigade.baka-wolf.com/downloads.php?do=file&act=down&id=172'
		dopost=2
		abstract='//by non7top'
		category=53
		search=1
		login=self.pppoename #'ep2738174_ll01'
		password= self.pppoepass #'egrvaitg'

		params = urllib.urlencode({'url' : url,
								   'dopost' : dopost, 
								   'abstract':abstract, 
								   'category':category, 
								   'search':1, 
								   'login':login, 
								   'password':password
								   })
		#self.basic_username = '2738174_ll'
		#self.basic_password = '201216'            # a very bad password
		#print params
	
		req = urllib2.Request(theurl, params)
		try:
			handle = urllib2.urlopen(req)
		except IOError, e:
			# here we *want* to fail
			pass
		else:
			# If we don't fail then the page isn't protected
			print "This page isn't protected by authentication."
			#sys.exit(1)
			
		if not hasattr(e, 'code') or e.code == 502:
			# we got an error - but not a 401 error
			print "This page isn't protected by authentication."
			print 'But we failed for another reason.'
			#sys.exit(1)
			
		authline = e.headers['www-authenticate']
		# this gets the www-authenticate line from the headers
		# which has the authentication scheme and realm in it
			
			
		authobj = re.compile(
			r'''(?:\s*www-authenticate\s*:)?\s*(\w*)\s+realm=['"]([^'"]+)['"]''',
			re.IGNORECASE)
		# this regular expression is used to extract scheme and realm
		matchobj = authobj.match(authline)
			
		#if not matchobj:
			# if the authline isn't matched by the regular expression
			# then something is wrong
			#print 'The authentication header is badly formed.'
			#print authline
			#sys.exit(1)
		
		#scheme = matchobj.group(1)
		#realm = matchobj.group(2)
		# here we've extracted the scheme
		# and the realm from the header
		#if scheme.lower() != 'basic':
		#    print 'This example only works with BASIC authentication.'
		#    sys.exit(1)
		
		base64string = base64.encodestring(
						'%s:%s' % (self.basic_username, self.basic_password))[:-1]
		authheader =  "Basic %s" % base64string
		req.add_header("Authorization", authheader)
		#print authheader
		#try:
		handle = urllib2.urlopen(req)
		#except IOError, e:
		#    # here we shouldn't fail if the username/password is right
		#    print "It looks like the username or password is wrong."
		#    sys.exit(1)
		thepage = handle.read()
		#print thepage
		
	def check(self):
		theurl = 'http://litops.hq.aaanet.ru/cts_support/cts_s_jinn'
		base64string = base64.encodestring(
						'%s:%s' % (self.basic_username, self.basic_password))[:-1]
		authheader =  "Basic %s" % base64string
		req = urllib2.Request(theurl)
		req.add_header("Authorization", authheader)
		try:
			handle = urllib2.urlopen(req)
			thepage = handle.read()
			#print thepage
		
			parser = etree.HTMLParser()
			tree  = etree.parse(StringIO(thepage), parser)
		
			r=tree.xpath('/html/body/table/tr/td/table[5]/tr/td[2]/table/tr/td/table/tr/td[2]/table/tr[4]/td/table/tr/td/font/table/tr[2]/td[4]/span')
			r1=tree.xpath('/html/body/table/tr/td/table[5]/tr/td[2]/table/tr/td/table/tr/td[2]/table/tr[4]/td/table/tr/td/font/table/tr[4]/td[4]/span')
			#print len(r[0].text), len(r1[0].text)
			#return 1
			if len(r[0].text) == 21 or len(r[0].text) == 1 or len(r[0].text) == 32:
					#print 'ok'
				return 1
			#elif len(r[0].text) == 23 and len(r1[0].text) == 1:
				#return 1
			else:
				#print 'false'
				return 0
		except:
			return 0
			#print len(r[0].text)
			#print len(r)
	

#qqq=jinn()
#qqq.check()
