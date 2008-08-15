#!/utsr/bin/env python
# -*- coding: utf8 -*-

from lib import webget
from necroposter import necroposter
from lib import utils

wg = webget()
wg.init_cookie("prizident", "yytonj")
k = wg.upload_file("/home/non7top/Desktop/1")
print utils.getnum(utils.get_urls_meta(k[2]))
