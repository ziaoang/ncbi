# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

import re

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class PubmedDetailSpider(scrapy.Spider):
    name = "pubmed_detail"
    start_urls = []

    def __init__(self):
        self.clear()
        for line in open("url1.txt"):
            t = line.strip().split('\t')
            if t[3] == 'Free PMC Article':
                self.start_urls.append(t[2])

    def parse(self, response):
        pmc_link = "http://www.ncbi.nlm.nih.gov" + response.xpath('//a[@class="status_icon"]/@href').extract()[0]
        yield Request(url=pmc_link, callback=self.after_get)

    def after_get(self, response):
        referer = response.request.headers['Referer']
        pdf_link = 'NULL'
        download_link = response.xpath('//div[@class="format-menu"]/ul/li/a/@href').extract()
        for link in download_link:
            if ".pdf" in link:
                pdf_link = "http://www.ncbi.nlm.nih.gov" + link
                break
        self.save("%s\t%s"%(referer, pdf_link))

    def save(self, line):
        df = open("url2.txt", "a")
        df.write("%s\n" % line)
        df.close()

    def clear(self):
        df = open("url2.txt", "w")
        df.close()

    def clean(self, text):
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text



