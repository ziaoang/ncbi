# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

import re
import json
import random

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class FreeSPSpider(scrapy.Spider):
    name = "freeSP"
    start_urls = []

    def __init__(self):
        todo_set = set()
        pmid_url = {}
        for line in open('src/free.txt'):
            t = line.strip().split('\t')
            pmid = t[0]
            if len(t) > 1:
                for i in range((len(t) - 1) / 2):
                    if t[2*i + 1] == "Springer":
                        todo_set.add(pmid)
                        pmid_url[pmid] = t[2*i + 2]
        
        have_set = set()
        for line in open('src/free_sp.txt'):
            t = line.strip().split('\t')
            pmid = t[0]
            have_set.add(pmid)
        
        print '-' * 20
        print "todo %d papers" % len(todo_set)
        print "have %d papers" % len(have_set)
        print "try %d papers" % len(todo_set - have_set)
        print '-' * 20
        
        for pmid in todo_set - have_set:
            self.start_urls.append(pmid_url[pmid] + "?pmid=%s"%pmid)

    def parse(self, response):
        pmid = response.request.meta['redirect_urls'][0].split('=')[-1]
        try1 = response.xpath('//a[@id="pdf-link"]/@href').extract()
        try2 = response.xpath('//a[@id="abstract-actions-download-article-pdf-link"]/@href').extract()
        pdf_link = 'NULL'
        if len(try1) == 1:
            pdf_link = "http://rd.springer.com" + try1[0]
        elif len(try2) == 1:
            pdf_link = "http://rd.springer.com" + try2[0]
        self.save("%s\t%s"%(pmid, pdf_link))

    def save(self, line):
        df = open("src/free_sp.txt", "a")
        df.write("%s\n" % line)
        df.close()



