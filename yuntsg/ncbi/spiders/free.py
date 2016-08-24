# -*- coding: utf-8 -*-
import scrapy

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class FreeSpider(scrapy.Spider):
    name = "free"
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
        out = []
        pmid = response.url.split('/')[-1]
        out.append(pmid)
        links = response.xpath('//div[@class="icons portlet"]/a')
        for link in links:
            way = link.xpath('./img/@alt').extract()[0].replace("Icon for ", "")
            url = link.xpath('./@href').extract()[0]
            out.append(way)
            out.append(url)
        self.save('\t'.join(out))

    def save(self, line):
        df = open("src/free.txt", "a")
        df.write("%s\n" % line)
        df.close()

    def clear(self):
        df = open("src/free.txt", "w")
        df.close()


