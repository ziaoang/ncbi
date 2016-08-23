# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

import re
import json

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class ListSpider(scrapy.Spider):
    name = "list"
    start_urls = []
    cookies = {}

    def __init__(self):
        self.load_cookies()

        free_set = set()
        for line in open("src/free2.txt"):
            t = line.strip().split('\t')
            free_set.add(t[0])

        have_set = set()
        for line in open("src/list.txt"):
            t = line.strip().split('\t')
            have_set.add(t[0])

        todo_set = set()
        for line in open("data/retrieval.txt"):
            t = line.strip().split('\t')
            todo_set.add(t[1])

        print '-' * 20
        print 'retrieval %d papers' % len(todo_set)
        print 'have %d papers' % len(have_set)
        print 'free %d papers' % len(free_set)
        print 'apply %d papers' % len(todo_set - have_set - free_set)
        print '-' * 20

        for pmid in todo_set - have_set - free_set:
            self.start_urls.append("http://nc.yuntsg.com/paddjsonp.do?pmid=%s" % pmid)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        pass

    def load_cookies(self):
        for line in open("data/cookies.txt"):
            if line[0] == '#':
                continue
            t = line.strip().split('\t')
            if len(t) == 7 and (t[0] == '.yuntsg.com' or t[0] == 'nc.yuntsg.com'):
                self.cookies[t[5]] = t[6]


