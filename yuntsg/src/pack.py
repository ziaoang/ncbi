import os
import re

def clean(text):
    text = re.sub(r'[^a-zA-Z]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

index = 0
query_index = {}
for line in open("data/query.txt"):
    index += 1
    query = line.strip()
    query_index[query] = index

    if not os.path.exists("pdf/pack/%d" % index):
        os.makedirs("pdf/pack/%d" % index)

cnt = 0
for line in open("data/retrieval.txt"):
    query, pmid, title = line.strip().split('\t')
    index = query_index[query]
    title = pmid + ' - ' + clean(title)[:64]
    if os.path.exists("pdf/merge/%s.pdf" % pmid) and not os.path.exists("pdf/pack/%d/%s.pdf" % (index, title)):
        cnt += 1
        order = "cp 'pdf/merge/%s.pdf' 'pdf/pack/%d/%s.pdf'" % (pmid, index, title)
        os.system(order)

print '-' * 20
print 'pack %d papers' % cnt
print '-' * 20



