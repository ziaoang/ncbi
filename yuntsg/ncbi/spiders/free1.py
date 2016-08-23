# -*- coding: utf-8 -*-
import scrapy

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Free1Spider(scrapy.Spider):
    name = "free1"
    start_urls = []

    def __init__(self):
        self.clear()

        todo_set = set()
        for line in open("data/retrieval.txt"):
            t = line.strip().split('\t')
            todo_set.add(t[1])

        print '-' * 20
        print "todo %d papers" % len(todo_set)
        print '-' * 20
        
        for pmid in todo_set:
           self.start_urls.append("http://www.ncbi.nlm.nih.gov/pubmed/%s" % pmid)

    def parse(self, response):
        pmc_info = response.xpath('//a[@class="status_icon"]/@href').extract()
        if len(pmc_info) == 1:
            pmid = response.url.split('/')[-1]
            self.save(pmid)

    def save(self, line):
        df = open("src/free1.txt", "a")
        df.write("%s\n" % line)
        df.close()

    def clear(self):
        df = open("src/free1.txt", "w")
        df.close()


