import os

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
folder_path = "pdf/merge"

todo_dict = dict()
for line in open("src/list.txt"):
    pmid, title, url = line.strip().split('\t')
    if url != 'NULL':
        todo_dict[pmid] = url

for pmid in todo_dict:
    url = todo_dict[pmid]
    file_path = "%s/%s.pdf" % (folder_path, pmid)
    order = "wget --tries=20 -c -P '%s' -U '%s' '%s' -O '%s'" % (folder_path, user_agent, url, file_path) # -c means continue for broken files
    os.system(order)

print '-' * 20
print "download %d papers" % len(todo_dict)
print '-' * 20


