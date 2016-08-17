from collections import defaultdict

pool = defaultdict(lambda:'NULL')
for line in open("url2.txt"):
    pubmed_url, pdf_url = line.strip().split('\t')
    pool[pubmed_url] = pdf_url

df = open("url.txt", "w")
for line in open("url1.txt"):
    query, title, pubmed_url, free_flag = line.strip().split('\t')
    df.write("%s\t%s\t%s\t%s\t%s\n"%(query, title, pubmed_url, free_flag, pool[pubmed_url]))
df.close()


