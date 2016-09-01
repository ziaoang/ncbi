import os
import re

def clean(text):
    text = re.sub(r'[^a-zA-Z]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

index = {}
for line in open("data/retrieval.txt"):
    query, pmid, title = line.strip().split('\t')
    index[pmid] = pmid + ' - ' + clean(title)[:64]

for i in range(10):
    if not os.path.exists("pdf/pack_%d" % i):
        os.system("mkdir pdf/pack_%d" % i)

cnt = 0
for pmid in index:
    filename = index[pmid]
    if os.path.exists("pdf/merge/%s.pdf" % pmid):
        cnt += 1
        order = "cp 'pdf/merge/%s.pdf' 'pdf/pack_%d/%s.pdf'" % (pmid, int(pmid) % 10, filename)
        os.system(order)
    elif os.path.exists("pdf/manual/%s.pdf" % pmid):
        cnt += 1
        order = "cp 'pdf/manual/%s.pdf' 'pdf/pack_%d/%s.pdf'" % (pmid, int(pmid) % 10, filename)
        os.system(order)

print '-' * 20
print 'pack %d papers' % cnt
print '-' * 20


