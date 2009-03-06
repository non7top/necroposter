#!/usr/bin/env python
# -*- coding: utf8 -*-


import sys
import os

import base64
import re
import urllib
import urllib2
from StringIO import StringIO
import logging

from lxml import etree

from necrolib import utils
from necrolib import datadir
from cast import cast
from cache import cache

logging.basicConfig(level=logging.DEBUG)

class necroposter():
        def __init__(self):
                logging.debug ("Init necroposter class")
                self.parser = etree.HTMLParser()
                self.homedir = datadir.user_data_dir("necroposter")
                logging.info ("Datadir is: %s" % self.homedir)
                self.chkdirs()
                self.caching = 1
                cachedir=os.path.join (self.homedir, "cache")
                self.cache = cache (cachedir)

        def dw_wapage(self,  wa_addr):
                logging.debug ( "Start dw_wapage" )
                self.pagenum = utils.getnum(wa_addr)
                self.wa_addr = "http://www.world-art.ru/animation/animation.php?id=%s" % self.pagenum
                fname=self.pagenum + '.cache'
                
                # TODO: gzip the cache
                page_body = self.cache.dw_html(self.wa_addr, fname)
                self.thepage = unicode(page_body, "cp1251")
                self.tree = etree.parse(StringIO(self.thepage), self.parser)

        def get_title(self):
                logging.debug ("Start get_title")
                r = self.tree.xpath('/html/body/center[2]/table[6]/tr/td/table/tr/td[5]/table[2]/tr/td[3]/font/b')
                self.title = r[0].text[:-2].strip()
                logging.debug ( "Got title: %s" % self.title )
                return self.title

        def get_year(self):
                logging.debug ("Starting get_year")
                r = self.tree.xpath("/html/body/center/table[6]/tr/td/table/tr/td[5]/table/tr/td[3]/a/font")
                self.year = r[0].text.strip()
                return self.year
                
        def get_names(self):
                self.names=[]
                r = self.tree.xpath("/html/body/center/table[6]/tr/td/table/tr/td[5]/table/tr/td[3]/br")
                for q in r:
                    if q.tail != None:
                        self.names.append(q.tail)
                return self.names
        
        def get_jenres(self):
                self.jenres=[]
                p = "//a[starts-with(@href, 'list.php?genre')]"
                r = self.tree.xpath(p)
                for q in r:
                        self.jenres.append(q.text)
                return self.jenres
        
        def get_type(self):
                p="/html/body/center/table[6]/tr/td/table/tr/td[5]/table/tr/td[3]/font[3]/b[3]"
                #p="/html/body/center/table[6]/tbody/tr/td/table/tbody/tr/td[5]/table[1]/tbody/tr/td[3]/font[2]/b[3]"
                r = self.tree.xpath(p)
                self.type = r[0].tail[2:]
                return self.type
        
        def get_episodes(self):
                try:
                        self.episodes=[]
                        p = "//table[.  = '" + u'Эпизоды:' + "']"
                        r = self.tree.xpath(p)[0].getnext().getnext()
                        rr = r.xpath("tr/td[1]")
                        self.episodes.append( rr[0].text )
                        
                        rrr = r.xpath('tr/td[1]/br')
                        for q in rrr:
                                self.episodes.append(q.tail)
                        self.has_ep = 1
                        return self.episodes
                except:
                        self.has_ep = 0
                        logging.warning ("Single episode")
                        return 0

        def get_series(self):
                try:
                        self.series = []
                        p = "//table[.  = '" + u'В каком порядке лучше смотреть эту серию:' + "']"
                        r = self.tree.xpath(p)[0].getnext().getnext()
                        
                        '''прогоняем по списку серий'''
                        for q in r:
                                rr = q.xpath('td[3]/a')
                                self.series.append(rr[0].text + rr[0].tail)
                        self.has_s = 1
                        return self.series
                except:
                        logging.warning ("Single serie")
                        self.has_s = 0
                        return 0
        
        def get_desc(self):
                try:
                        p = "//table[.  = '" + u'Краткое содержание:' + "']"
                        r = self.tree.xpath(p)[0].getnext().getnext()
                        rr=r.xpath('tr/td/p')
                        self.desc=rr[0].text
                except:
                        self.desc = 0
                        logging.warning ("No description found")

        
        def get_actors(self):
            c=cast(self.pagenum)
            self.actors=c.get_actors()
        
        def get_imglink(self):
                logging.debug ("Start get_imglink")
                #p="/html/body/center/table[6]/tr/td/table/tr/td[5]/table[1]/tr/td[1]/a[1]/img"
                p="//img[starts-with(@src, 'img/')]"
                r = self.tree.xpath(p)
                link='http://www.world-art.ru/animation/' + r[0].get("src")
                logging.debug ("Image link is: %s" % link)
                #fname2=r[0].get("alt") + '.jpg'
                fname2=self.pagenum + '.jpg'
                fname=os.path.join (self.homedir, "cover/" + fname2)
                logging.debug ("Poster filename is: %s" % fname)
                self.imglink={'imglink':link,  'fname':fname}
                return self.imglink

        def get_director(self):
                p = "//b[. = '" + u'Режиссёр' + "']"
                r = self.tree.xpath(p)[0].getnext()
                '''дергаем номер режиссера из линки'''
                num = utils.getnum (r.get("href"))
                link="http://world-art.ru/people.php?id=%s" % num
                self.director = {'name': r.text, 'num': num, 'link': link}

        '''вытаскиваем номер студии, генерим ссылки и скачиваем эмблему студии'''
        def get_studio(self):
                p = "//a[starts-with(@href, 'company_film.php')]"
                r = self.tree.xpath(p)
                '''дергаем номер студии из линки'''
                self.studio = {'num': utils.getnum(r[0].get("href"))}
                '''генерим ссылку на картинку и ссылку на оптсание студии'''
                self.studio['link'] = "http://world-art.ru/animation/company_film.php?id=%s" %self.studio['num']
                self.studio['imglink'] = "http://www.world-art.ru/img/company/%s.jpg" %self.studio['num']
                self.studio['fname'] = os.path.join (self.homedir, "studio/%s.jpg" %self.studio['num'])
                
                '''качаем эмблему студии'''
                self.cache.dw_img(self.studio['imglink'], self.studio['fname'])
                logging.info ("Studio emblem: %s" %self.studio['fname'])
        
        def init_data(self):
                logging.debug ("Start init_data")
                self.get_title()
                self.get_year()
                self.get_names()
                self.get_jenres()
                self.get_type()
                self.get_episodes()
                self.get_series()
                self.get_desc()
                self.get_director()
                self.get_actors()
                il=self.get_imglink()
                self.get_studio()
                self.cache.dw_img(il['imglink'], il['fname'], self.wa_addr)
                logging.debug ("Finished init_data")

        def gen_bbcode(self):
                tpl="[b][size=4]%s[/size] [color=#8B0000][%s][/color][/b]\n" % (self.title, self.year)
                tpl += "\n"
                for q in self.names:
                        tpl += q + "\n"
                tpl += "\n"
                
                tpl+= "[img]http://fstore5.aaanet.ru:8080/139780/placeholder.png[/img]\n\n"
                
                tpl += u"[b]Производство:[/b] Япония\n"
                
                tpl += u"[b]Жанр:[/b] "
                for q in self.jenres:
                        tpl += q + ", "
                tpl = tpl[:-2]
                tpl += "\n"
                
                tpl += u"[b]Тип:[/b] %s" % self.type
                tpl += "\n"
                
                tpl += u"[b]Режиссёр:[/b] [url=" + self.director['link'] + ']' + self.director['name'] + '[/url]'
                tpl += "\n"

                k=0
                tpl += u'[b]Роли озвучивали:[/b] '
                for ac in self.actors:
                    k += 1
                    if k <= 5:
                        tpl += '[url=' + ac['ac_link'] + ']' + ac['ac_name'] + '[/url]' + ' (' + ac['ac_role'] + '), '


                tpl = tpl[:-2]

                tpl += "\n"
                tpl += "\n"
                
                tpl += "[url=%s][img]http://fstore5.aaanet.ru:8080/139774/world-art-logo.png[/img][/url]" % self.wa_addr
                tpl += " [url=%s][img]=STUDIO_IMG_LINK=[/img][/url]" % self.studio['link']
                tpl += "\n"
                tpl += "\n"
                
                '''Description'''
                if self.desc != 0:
                        tpl += u"[b]Краткое содержание:[/b]\n"
                        tpl += self.desc
                        tpl += "\n"
                        tpl += "\n"

                """episodes list"""
                if self.has_ep != 0:
                        tpl += u"[b]Эпизоды:[/b]\n"
                        for q in self.episodes:
                                if q != None:
                                        tpl += q + "\n"
                        tpl += "\n"
                        tpl += "\n"
                
                """series list"""
                if self.has_s != 0:
                        tpl += u"[b]В каком порядке лучше смотреть эту серию:[/b]\n"
                        for q in self.series:
                                if q != None:
                                        tpl += q + "\n"
                        tpl += "\n"
                        tpl += "\n"
                
                tpl += u"[url=http://file.aaanet.ru/?search=][b]Скачать[/b][/url]"
                #print "_________cut_here_________"
                #print tpl
                #print "_________/cut_here_________"
                
                #print self.imglink['fname']
                #print self.studio['fname']
                return tpl
        
        def gen_spark(self):
                tpl=self.title

#                tpl += "\n"
#                for q in self.names:
#                        tpl += q + "\n"
#                tpl += "\n-----------------------------\n"
                
                tpl += u"Жанр: "
                for q in self.jenres:
                        tpl += q.capitalize() + ", "
                tpl = tpl[:-2]
                tpl += "\n"

                tpl += u"Производство: Япония\n"                

                tpl += u"Режиссёр: " + self.director['name']
                tpl += "\n"
                
                tpl += u"Продолжительность: %s" % self.type
                tpl += "\n\n"
                
                tpl += self.year
                tpl += "\n\n"

                k=0
                tpl += u'Роли озвучивали:'
                for ac in self.actors:
                    k += 1
                    if k <= 5:
                        tpl += '[url=' + ac['ac_link'] + ']' + ac['ac_name'] + '[/url]' + ' (' + ac['ac_role'] + '), '


                tpl = tpl[:-2]
                tpl += "\n\n"

                '''Description'''
                if self.desc != 0:
                        tpl += u"[b]Краткое содержание:[/b]\n"
                        tpl += self.desc
                        tpl += "\n"
                        tpl += "\n"

                tpl += "\n"
                tpl += "\n"
                
                tpl += u"[url=%s]Описание на World-Art.ru[/url]" % self.wa_addr
                tpl += "\n"
                tpl += "\n-----------------------------\n"
                


                """episodes list"""
                if self.has_ep != 0:
                        tpl += u"[expand=\"Эпизоды\"]"
                        for q in self.episodes:
                                if q != None:
                                        tpl += q + "\n"
                        tpl += "[/expand]\n"
                        tpl += "\n"
                
                """series list"""
                if self.has_s != 0:
                        tpl += u"[expand=\"В каком порядке лучше смотреть эту серию\"]"
                        for q in self.series:
                                if q != None:
                                        tpl += q + "\n"
                        tpl += "[/expand]\n"
                        tpl += "\n"
                
                #print "_________cut_here_________"
                #print tpl
                #print "_________/cut_here_________"
                
                #print self.imglink['fname']
                #print self.studio['fname']
                return tpl
        
        def chkdirs(self):
                self.mkdir(os.path.join (self.homedir ,'studio'))
                self.mkdir(os.path.join (self.homedir, 'cover'))
                self.mkdir(os.path.join (self.homedir, 'cache'))
                self.mkdir(os.path.join (self.homedir, 'mini'))

        def mkdir(self, dir):
                if not os.path.isdir(dir):
                        os.makedirs(dir)
                
        def cat(self, r):
                print etree.tostring(r[0])

        def lsch(self, xpath):
                r = self.tree.xpath(xpath)
                for c in r[0]:
                        print c.tag
                pass
        

def main(n):
        if len(n) == 0:
                print "Give pagenumber or full link as an argument"
                sys.exit(1)
        else:
                np=necroposter()
                np.dw_wapage(n[0])
                #print np.get_episodes()
                np.init_data()
                #print np.gen_bbcode()
                print np.gen_spark()
                
if __name__ == "__main__":
    main(sys.argv[1:])
