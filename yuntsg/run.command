#!/usr/bin/env python

import os
import sys

path = os.path.dirname(sys.argv[0])
os.chdir(path)


os.system("scrapy runspider ncbi/spiders/list.py")
os.system("scrapy runspider ncbi/spiders/retrieval.py")
os.system("python src/merge.py")
os.system("scrapy runspider ncbi/spiders/apply.py")
os.system("python src/download.py")


