x1 = int(input())
y1 = int(input())
x2 = int(input())
y2 = int(input())
x3 = int(input())
y3 = int(input())

ab = (x2-x1)**2 + (y2-y1)**2
bc = (x3-x2)**2 + (y3-y2)**2
ac = (x3-x1)**2 + (y3-y1)**2

if ab + bc == ac or ab + ac == bc or bc + ac == ab:
    print('yes')
else:
    print('no')

