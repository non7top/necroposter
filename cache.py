#!/usr/bin/env python
# -*- coding: utf8 -*

import os
import urllib
import urllib2
from StringIO import StringIO
import logging


class cache():
    def __init__ (self, storage, referer=None, enable = 1):
        if not os.path.isdir(storage):
            os.makedirs(storage)
        self.storage=storage
        self.referer=referer


    def get(self, fname):
        k = os.path.join(self.storage, fname)
        l = open(k)
        m = l.read()
        l.close()
        return m

    def put(self, fname, content):
        k = os.path.join(self.storage, fname)
        l = open(k, 'w')
        n = l.write(content)
        l.close()
        return n

    def incache(self, fname):
        k = os.path.join(self.storage, fname)
        if os.path.isfile(k):
            return 1
        else:
            return 0

    def dw_html(self, url, fname):
        if self.incache(fname):
            logging.debug ("Not re-downloading file")
            page_body=self.get(fname)
        else:
            #logging.info( "WA page is %s" % self.wa_addr )
            req = urllib2.Request(url)

            try:
                handle = urllib2.urlopen(req)
            except IOError:
                print "ioerror"
            page_body=handle.read()
            handle.close()
            self.put(fname,page_body)
        return page_body

    def dw_img(self, url, fname):
        if self.incache(fname):
            logging.debug ("Not re-downloading image file")
        else:
            logging.info ( ("Downloading link %s to file %s") % (url, fname) )
            req = urllib2.Request(url)
            if self.referer != None:
                req.add_header("Referer", self.referer)
            try:
                handle = urllib2.urlopen(req)
            except IOError, e:
                logging.warning( "IOerror %s" % e)
            data = handle.read()
            handle.close()
            self.put(fname, data)

