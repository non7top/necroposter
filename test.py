#!/utsr/bin/env python
# -*- coding: utf8 -*-

import sys
import base64
import re
import urllib
import urllib2
from StringIO import StringIO

from lxml import etree
from necroposter import necroposter

np=necroposter()
np.dw_wapage("3284")
np.init_data()
#np.get_desc()
#np.get_director()
np.gen_bbcode()

