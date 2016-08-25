import os

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
folder_path = "pdf/merge"

todo_set = set()
for line in open("data/retrieval.txt"):
    query, pmid, title = line.strip().split('\t')
    todo_set.add(pmid)

have_set = set()
for name in os.listdir("pdf/merge"):
    if ".pdf" in name:
        have_set.add(name.split(".")[0])

print '-' * 20
print 'todo %d papers' % len (todo_set)
print 'have %d papers' % len (have_set)
print 'try %d papers' % len (todo_set - have_set)
print '-' * 20

pmid_pdf = {}
for line in open("src/free_pmc.txt"):
    pmid, url = line.strip().split('\t')
    if pmid in todo_set - have_set and url != 'NULL':
        pmid_pdf[pmid] = url

for line in open("src/free_sp.txt"):
    pmid, url = line.strip().split('\t')
    if pmid in todo_set - have_set and url != 'NULL':
        pmid_pdf[pmid] = url

for line in open("src/list.txt"):
    pmid, url = line.strip().split('\t')
    if pmid in todo_set - have_set and url != 'NULL':
        pmid_pdf[pmid] = url

print '-' * 20
print "download %d papers" % len(pmid_pdf)
print '-' * 20

for pmid in pmid_pdf:
    url = pmid_pdf[pmid]
    file_path = "%s/%s.pdf" % (folder_path, pmid)
    # order = "wget --tries=20 -c -P '%s' -U '%s' '%s' -O '%s'" % (folder_path, user_agent, url, file_path) # -c means continue for broken files
    order = "wget -P '%s' -U '%s' '%s' -O '%s'" % (folder_path, user_agent, url.replace(r"'", r"%27"), file_path)
    print order
    os.system(order)

print '-' * 20
print "download %d papers" % len(pmid_pdf)
print '-' * 20



