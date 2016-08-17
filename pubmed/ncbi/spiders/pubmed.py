# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest

import re

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class PubmedSpider(scrapy.Spider):
    name = "pubmed"
    start_urls = []

    def __init__(self):
        self.clear()
        for line in open("query.txt"):
            self.start_urls.append("http://www.ncbi.nlm.nih.gov/pubmed/?term=%s" % (line.strip().replace(" ", "+")))
            break

    def parse(self, response):
        query = response.url.split("=")[-1]

        page_info = response.xpath('//h3[@class="result_count left"]/text()').extract()[0]
        result_count = int(page_info.split(' ')[-1])
        page_count = (result_count - 1) / 100 + 1

        print "-" * 20
        print "query: %s" % query
        print "result count: %d" % result_count
        print "page count: %d" % page_count
        print "-" * 20

        for i in range(page_count):
            yield FormRequest(url="http://www.ncbi.nlm.nih.gov/pubmed",
                              formdata={
                                  'term': query,
                                  'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_DisplayBar.PageSize': '100',
                                  'EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Entrez_Pager.CurrPage': '%d'%(i+1),
                                  'EntrezSystem2.PEntrez.DbConnector.LastQueryKey': '1',
                                  'EntrezSystem2.PEntrez.DbConnector.Cmd': 'displaychanged'
                              },
                              callback=self.after_post)

    def after_post(self, response):
        query = response.xpath('//input[@id="term"]/@value').extract()[0]
        items = response.xpath('//div[@class="rprt"]')
        for item in items:
            title = ''.join(item.xpath('./div[@class="rslt"]/p[@class="title"]/a//text()').extract())
            detail = "http://www.ncbi.nlm.nih.gov" + item.xpath('./div[@class="rslt"]/p[@class="title"]/a/@href').extract()[0]
            free_info = 'NULL'
            free = item.xpath('./div[@class="rslt"]/div[@class="aux"]/div[@class="resc"]/a/text()')
            if len(free) == 1:
                free_info = free.extract()[0]
            self.save("%s\t%s\t%s\t%s"%(query, self.clean(title), detail, free_info))

    def save(self, line):
        df = open("url1.txt", "a")
        df.write("%s\n" % line)
        df.close()

    def clear(self):
        df = open("url1.txt", "w")
        df.close()

    def clean(self, text):
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text



