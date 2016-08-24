# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

import re
import json
import random

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class FreePMCSpider(scrapy.Spider):
    name = "freePMC"
    start_urls = []

    def __init__(self):
        todo_set = set()
        pmid_url = {}
        for line in open('src/free.txt'):
            t = line.strip().split('\t')
            pmid = t[0]
            if len(t) > 1:
                for i in range((len(t) - 1) / 2):
                    if t[2*i + 1] == "PubMed Central":
                        todo_set.add(pmid)
                        pmid_url[pmid] = t[2*i + 2]
        
        have_set = set()
        for line in open('src/free_pmc.txt'):
            t = line.strip().split('\t')
            pmid = t[0]
            have_set.add(pmid)
        
        print '-' * 20
        print "todo %d papers" % len(todo_set)
        print "have %d papers" % len(have_set)
        print "try %d papers" % len(todo_set - have_set)
        print '-' * 20
        
        for pmid in todo_set - have_set:
            self.start_urls.append(pmid_url[pmid])

    def parse(self, response):
        pmid = response.request.meta['redirect_urls'][0].split('/')[-2]
        pdf_link = 'NULL'
        download_link = response.xpath('//div[@class="format-menu"]/ul/li/a/@href').extract()
        for link in download_link:
            if ".pdf" in link:
                pdf_link = "http://www.ncbi.nlm.nih.gov" + link
                break
        self.save("%s\t%s"%(pmid, pdf_link))

    def save(self, line):
        df = open("src/free_pmc.txt", "a")
        df.write("%s\n" % line)
        df.close()



