#!/usr/bin/env python

import os
import sys

path = os.path.dirname(sys.argv[0])
os.chdir(path + '/..')

os.system("python src/merge.py")


