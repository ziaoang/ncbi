import os

history = {}

if os.path.exists("src/all_retrieval.txt"):
    sf = open("src/all_retrieval.txt", "r")
    for line in sf:
        query, pmid, title = line.strip().split('\t')
        if query not in history:
            history[query] = set()
        history[query].add(pmid)
    sf.close()

cnt = 0
df = open("src/all_retrieval.txt", "a")
for line in open("data/retrieval.txt"):
    query, pmid, title = line.strip().split('\t')
    if query in history and pmid in history[query]:
        continue
    cnt += 1
    df.write("%s\t%s\t%s\n" % (query, pmid, title))
df.close()

print '-' * 20
print "add %d query-paper pairs" % cnt
print '-' * 20


