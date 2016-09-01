import os

pmid_title = {}

todo_set = set()
for line in open("data/retrieval.txt"):
    query, pmid, title = line.strip().split('\t')
    todo_set.add(pmid)
    pmid_title[pmid] = title

have_set = set()
for name in os.listdir("pdf/merge"):
    if ".pdf" in name:
        have_set.add(name.split(".")[0])
for name in os.listdir("pdf/manual"):
    if ".pdf" in name:
        have_set.add(name.split(".")[0])

print '-' * 20
print 'todo %d papers' % len (todo_set)
print 'have %d papers' % len (have_set)
print 'manual %d papers' % len (todo_set - have_set)
print '-' * 20

df = open("pdf/manual/miss.txt", "w")
for pmid in todo_set - have_set:
    df.write( "%s\t%s\n" % (pmid, pmid_title[pmid]) )
df.close()


