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

import urllib
import urllib2
import re
import md5
#from PyQt4 import QtCore, QtGui
from lxml import etree
from StringIO import StringIO
import httplib, mimetypes
import urlparse
import random
import os

class webget:
    def __init__(self):
        self.init = 0
    def init_cookie(self, login, password):
        self.login = login
        m = md5.new()
        m.update(password)
        md5pass=m.hexdigest()
        #print login, password
        
        #req = urllib2.Request('http://file.aaanet.ru/')
        #f = urllib2.urlopen(req)
	#print f.headers
        #cookie = unicode(f.headers['Set-Cookie'], 'cp1251')
        #matches = re.findall('(?si)PHPSESSID=(.*?);', cookie)
        #self.sesid = matches[0]
        
        params = urllib.urlencode({'key' : md5pass, 'login' : login})
        #print params
        req = urllib2.Request('http://file.aaanet.ru/', params)
        req.add_header("Referer", "http://file.aaanet.ru/")
        #req.add_header("Cookie", "PHPSESSID=" + self.sesid)
        f2 = urllib2.urlopen(req)
        cookie2 = unicode(f2.headers['Set-Cookie'], 'cp1251')
        matches = re.findall('(?si)user_sid=(.*?);', cookie2)
        self.user_sid = matches[0]
        
        #self.cookie_value = "PHPSESSID=" + self.sesid + ";" + "user_sid=" + self.user_sid +";" + "file_agree=1"
	self.cookie_value = "user_sid=" + self.user_sid +";" + "file_agree=1"
        return self.cookie_value

    def fo_add_item(self, cookie_value, link, description, searchc):
        params=urllib.urlencode({'downfileweb':link, 'taskid':1, 'searchc':searchc, 'srch':1,'description':description })
        print params
        req = urllib2.Request('http://file.aaanet.ru/?webget=1', params)
        req.add_header("Referer", "http://file.aaanet.ru/?webget=1")
        req.add_header("Cookie", cookie_value)
        f = urllib2.urlopen(req)

    def post_multipart(self, fields, files):
        """
        Post fields and files to an http host as multipart/form-data.
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return the server's response page.
        """
        host = "upload%s.aaanet.ru" % random.randint(1,8)
        selector = "/cgi-bin/upload.cgi?ssid=%s" % random.randint(10**29, 10**30-1)
        content_type, body = self.encode_multipart_formdata(fields, files)
        h = httplib.HTTPConnection(host)
        headers = {
            'Content-Type': content_type,
            'Content-Length': len(body)
            }
        print selector, len(body)
        h.request('POST', selector, body, headers)
        res = h.getresponse()
        return res.status, res.reason, res.read()


    def encode_multipart_formdata(self, fields, files):
        """
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return (content_type, body) ready for httplib.HTTP instance
        """
        BOUNDARY = '-----------------------------112103091412995700021765477310'
        CRLF = '\r\n'
        L = []
        for (key, value) in fields:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)
        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % self.get_content_type(filename))
            L.append('')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        #print body
        return content_type, body

    def get_content_type(self,filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        #return 'application/octet-stream'

    def upload_file(self, fname, fields=1):
        if fields == 1:
            fields = self.uf_fields()
        upfile=[]
        upfile.append(("upfile", os.path.basename(fname), open(fname).read()))
        return self.post_multipart(fields,upfile)

    def uf_fields(self):
        fields=[]
        fields.append(('login',self.login))
        fields.append(('sesion_id',str(self.user_sid)))
        fields.append(('hcategory', '1'))
        fields.append(('hissearch', '1'))
        fields.append(('hdescription', ''))
        fields.append(('htags2add', ''))
        try:
                fields.append(('searchc',str(self.c)))
        except:
                fields.append(('searchc', '0'))
        fields.append(('srch', '1'))
        fields.append(('tags2add', ''))
        try:
                fields.append(('description', self.d))
        except:
                fields.append(('description', 'Test of automatic upload of files'))
        return fields

