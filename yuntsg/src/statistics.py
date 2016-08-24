from collections import defaultdict


total_cnt = 0
miss_cnt = 0

cnt = defaultdict(int)
for line in open('free.txt'):
    t = line.strip().split('\t')
    total_cnt += 1
    if len(t) == 1:
        miss_cnt += 1
    else:
        for i in range((len(t) - 1) / 2):
            cnt[t[2*i + 1]] += 1

print 'total cnt %d' % total_cnt
print 'miss cnt %d' % miss_cnt

to_sort = []
for name in cnt:
    to_sort.append([name, cnt[name]])
to_sort.sort(key=lambda x: x[1], reverse=True)

for i in range(10):
    print to_sort[i][0], to_sort[i][1]



