n = int(input())
p = int(input())

with open('data.txt') as f: 
    lst1 = []
    lst2 = []
    for token in f.read().strip().split(' '):
        if token.isdigit():
            lst1.append(str(int(token) ** p))
            if not int(token) % n:
                lst2.append(token)

with open('out-1.txt', 'w') as f:
    f.write(' '.join(lst2))

with open('out-2.txt', 'w') as f:
    f.write(' '.join(lst1))



