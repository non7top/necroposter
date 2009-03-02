import os, sys
from paste.request import parse_formvars
from Cheetah.Template import Template
from paste.debug import prints

cp=os.path.dirname(__file__)
sys.path.append(cp)
from necroposter import necroposter


def application(environ, start_response):
        fields = parse_formvars(environ)
        if environ['REQUEST_METHOD'] == 'GET':
                start_response('200 OK', [('content-type','text/html; charset=utf-8')])
                np=necroposter()
                np.dw_wapage(fields['wa_addr'])
                np.init_data()
                tpl=""
                for q in np.episodes:
                        if q != None:
                                    tpl += str(q) + "<br>\n"
                return [str(tpl)]
        else:
                start_response('200 OK', [('content-type', 'text/html; charset=utf-8')])
                tmpl_fl=os.path.join(cp, 'templates/form.tmpl')
                k=Template(file=tmpl_fl)
                return [str(k)]

        
