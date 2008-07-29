#!/utsr/bin/env python
# -*- coding: utf8 -*-


import httplib, mimetypes
import urlparse

def post_multipart(host, selector, fields, files):
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
    """
    content_type, body = encode_multipart_formdata(fields, files)
    h = httplib.HTTPConnection(host)
    headers = {
        'Content-Type': content_type,
        'Content-Length': len(body)
        }
    print selector, len(body)
    h.request('POST', selector+"?ssid=573353019141348328026271398987", body, headers)
    res = h.getresponse()
    return res.status, res.reason, res.read()


def encode_multipart_formdata(fields, files):
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
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    #print body
    return content_type, body

def get_content_type(filename):
    #return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    return 'application/octet-stream'

def posturl(url, fields, files):
    urlparts = urlparse.urlsplit(url)
    return post_multipart(urlparts[1], urlparts[2], fields,files)

fields=[]
fields.append(('login', 'prizident'))
fields.append(('sesion_id', '40a57e60d67f5e149cca2f3a8cad1ade'))
fields.append(('hcategory', '1'))
fields.append(('hissearch', '1'))
fields.append(('hdescription', ''))
fields.append(('htags2add', ''))
fields.append(('searchc', '0'))
fields.append(('srch', '1'))
fields.append(('tags2add', ''))
fields.append(('description', 'Test of automatic upload of files'))
print fields
upfile=[]
upfile.append(("upfile", "Keiko Lee - The Flame (JPOP.ru).mp3", open('/home/non7top/Desktop/Keiko Lee - The Flame (JPOP.ru).mp3').read()))
host="http://upload7.aaanet.ru/cgi-bin/upload.cgi?ssid=573353019141348328026271398987"

print posturl(host,fields,upfile)
