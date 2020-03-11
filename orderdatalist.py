import re
f = open('marketdata/datalist','r')
dates = []
for line in f:
  line = ''.join(x for x in line if x.isdigit())
  if not line.isnumeric():
    print('was not numeric')
    print(line)
    continue
  dates.append(int(line))

dates.sort()

# write file
with open('marketdata/datalistsorted','w')as f:
  for date in dates:
    f.write('%d\n' % date)
