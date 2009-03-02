#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sys
from paste.request import parse_formvars
from Cheetah.Template import Template
from paste.debug import prints

cp=os.path.dirname(__file__)
sys.path.append(cp)
from necroposter import necroposter

from fcgi import WSGIServer

def application(environ, start_response):
        fields = parse_formvars(environ)
        tplvars={"tpl":""}
        print fields
        if environ['REQUEST_METHOD'] == 'POST' and fields['wa_addr'] != "":
                np=necroposter()
                np.dw_wapage(fields['wa_addr'])
                np.init_data()
	        #print fields['doupload']
                tplvars['tpl']=str(np.gen_bbcode().encode('utf-8'))
                
		tplvars["page_id"]=np.pagenum       	
        else:
        	pass
	
        start_response('200 OK', [('content-type', 'text/html; charset=utf-8')])
	
        tmpl_fl=os.path.join(cp, 'templates/form.tmpl')
        k=Template(file=tmpl_fl,searchList=[tplvars])
        return [str(k)]

        
WSGIServer(application, bindAddress = '/tmp/fcgi.sock').run()
