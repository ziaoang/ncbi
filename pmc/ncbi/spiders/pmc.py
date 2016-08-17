# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest

import re

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class PmcSpider(scrapy.Spider):
    name = "pmc"
    start_urls = []

    def __init__(self):
        self.clear()
        for line in open("query.txt"):
            self.start_urls.append("http://www.ncbi.nlm.nih.gov/pmc/?term=%s" % (line.strip().replace(" ", "+")))
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
            yield FormRequest(url="http://www.ncbi.nlm.nih.gov/pmc",
                              formdata={
                                  'term': query,
                                  'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.PageSize': '100',
                                  'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Entrez_Pager.CurrPage': '%d'%(i+1),
                                  'EntrezSystem2.PEntrez.DbConnector.LastQueryKey': '1',
                                  'EntrezSystem2.PEntrez.DbConnector.Cmd': 'PageChanged'
                              },
                              callback=self.after_post)

    def after_post(self, response):
        query = response.xpath('//input[@id="term"]/@value').extract()[0]
        items = response.xpath('//div[@class="rprt"]')
        for item in items:
            title = ''.join(item.xpath('./div[@class="rslt"]/div[@class="title"]//text()').extract())
            pdf_link = 'NULL'
            links = item.xpath('./div[@class="rslt"]/div[@class="aux"]/div[@class="links"]/a/@href').extract()
            for link in links:
                if '.pdf' in link:
                    pdf_link = link
            if pdf_link != 'NULL':
                pdf_link = "http://www.ncbi.nlm.nih.gov" + pdf_link
            self.save("%s\t%s\t%s"%(query, self.clean(title), pdf_link))

    def save(self, line):
        df = open("url.txt", "a")
        df.write("%s\n" % line)
        df.close()

    def clear(self):
        df = open("url.txt", "w")
        df.close()

    def clean(self, text):
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text



