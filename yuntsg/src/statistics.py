from collections import defaultdict
import urlparse

total_cnt = 0
miss_cnt = 0

cnt = defaultdict(int)
detail = defaultdict(list)
for line in open('free.txt'):
    t = line.strip().split('\t')
    total_cnt += 1
    if len(t) == 1:
        miss_cnt += 1
    else:
        for i in range((len(t) - 1) / 2):
            cnt[t[2*i + 1]] += 1
            detail[t[2*i + 1]].append(t[2*i + 2])

print 'total cnt %d' % total_cnt
print 'miss cnt %d' % miss_cnt

to_sort = []
for name in cnt:
    to_sort.append([name, cnt[name]])
to_sort.sort(key=lambda x: x[1], reverse=True)

print len(cnt)
print len(detail)
host = defaultdict(set)
for name in detail:
    for url in detail[name]:
        t = urlparse.urlsplit(url)
        host[name].add(t.netloc)

for i in range(10):
    if len(host[to_sort[i][0]]) != 1:
        continue
    print '-' * 20
    print to_sort[i][0], to_sort[i][1]
    for url in host[to_sort[i][0]]:
        print url
    print '-' * 20



