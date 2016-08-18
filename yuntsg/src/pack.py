import os

if not os.path.exists("pdf/pack/need_to_rename"):
    os.makedirs("pdf/pack/need_to_rename")

cnt = 0
for line in open("data/retrieval.txt"):
    query, pmid, title = line.strip().split('\t')
    if os.path.exists("pdf/merge/%s.pdf" % pmid):
        if not os.path.exists("pdf/pack/need_to_rename/%s.pdf" % pmid):
            cnt += 1
            order = "cp pdf/merge/%s.pdf pdf/pack/need_to_rename/%s.pdf" % (pmid, pmid)
            os.system(order)

print '-' * 20
print "pack %d papers" % cnt
print '-' * 20


