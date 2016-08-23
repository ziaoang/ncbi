# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

import re
import json

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Free2Spider(scrapy.Spider):
    name = "free2"
    start_urls = []

    def __init__(self):
        have_set = set()
        for line in open("src/free2.txt"):
            t = line.strip().split('\t')
            have_set.add(t[0])

        todo_set = set()
        for line in open("src/free1.txt"):
            todo_set.add(line.strip())

        print '-' * 20
        print "todo %d papers" % len(todo_set)
        print "have %d papers" % len(have_set)
        print "try %d papers" % len(todo_set - have_set)
        print '-' * 20
        
        for pmid in todo_set - have_set:
          self.start_urls.append("http://www.ncbi.nlm.nih.gov/pubmed/%s" % pmid)

    def parse(self, response):
        pmc_info = response.xpath('//a[@class="status_icon"]/@href').extract()
        if len(pmc_info) == 1:
            yield Request(url="http://www.ncbi.nlm.nih.gov" + pmc_info[0], callback=self.next_parse)

    def next_parse(self, response):
        pdf_link = None
        download_link = response.xpath('//div[@class="format-menu"]/ul/li/a/@href').extract()
        for link in download_link:
            if ".pdf" in link:
                pdf_link = "http://www.ncbi.nlm.nih.gov" + link
                break
        if pdf_link:
            pmid = response.request.headers['Referer'].split('/')[-1]
            self.save("%s\t%s"%(pmid, pdf_link))

    def save(self, line):
        df = open("src/free2.txt", "a")
        df.write("%s\n" % line)
        df.close()


