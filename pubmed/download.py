import os

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"

for line in open("url.txt"):
    query, title, pubmed_url, free_flag, pdf_url = line.strip().split('\t')
    title = title.replace(":", "")
    folder_path = "pdf/need_to_rename"
    file_path = "%s/%s.pdf" % (folder_path, title)
    if pdf_url != 'NULL':
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        if not os.path.exists(file_path):
            order = "wget -P '%s' -U '%s' '%s' -O '%s'" % (folder_path, user_agent, pdf_url, file_path)
            os.system(order)


