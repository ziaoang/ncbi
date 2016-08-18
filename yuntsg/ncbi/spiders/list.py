# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

import re
import json

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class ApplySpider(scrapy.Spider):
    name = "apply"
    start_urls = []
    cookies = {}

    def __init__(self):
        self.clear()
        self.load_cookies()
        self.start_urls.append("http://nc.yuntsg.com/pinjsonp.do?page=1")

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        t = json.loads(response.body[5:-1])
        self.json_handle(t)
        allpage = int(t["allpage"])
        if allpage > 1:
            for page in range(2, allpage + 1):
                url = "http://nc.yuntsg.com/pinjsonp.do?page=%d" % page
                yield Request(url=url, cookies=self.cookies, callback=self.next_parse)

    def next_parse(self, response):
        t = json.loads(response.body[5:-1])
        self.json_handle(t)

    def json_handle(self, t):
        for paper in t["res"]:
            if len(paper['filepath']) == 0:
                self.save("%s\t%s\t%s" % (paper['pmid'], paper['ti'], 'NULL'))
            else:
                self.save("%s\t%s\t%s" % (paper['pmid'], paper['ti'], paper['filepath'][0]))

    def load_cookies(self):
        for line in open("data/cookies.txt"):
            if line[0] == '#':
                continue
            t = line.strip().split('\t')
            if len(t) == 7 and (t[0] == '.yuntsg.com' or t[0] == 'nc.yuntsg.com'):
                self.cookies[t[5]] = t[6]

    def save(self, line):
        df = open("src/list.txt", "a")
        df.write("%s\n" % line)
        df.close()

    def clear(self):
        df = open("src/list.txt", "w")
        df.close()


