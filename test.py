from bisect import bisect_left, bisect_right
l = [2,8,9,12,15,20,25,96,100]

s = l.index(l[bisect_right(l,16)])
e = l.index(l[bisect_left(l,18)])

print(s)
print(e)