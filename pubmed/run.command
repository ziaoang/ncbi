#!/usr/bin/env python

import os
import sys

path = os.path.dirname(sys.argv[0])
os.chdir(path)

os.system("scrapy runspider ncbi/spiders/pubmed.py")
os.system("scrapy runspider ncbi/spiders/pubmed_detail.py")
os.system("python merge.py")
os.system("python download.py")


