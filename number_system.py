__all__ = [
    'dec2bin',
    'dec2oct',
    'dec2hex',
    'bin2dec',
    'oct2dec',
    'hex2dec',
]

def to_system(number, system):
    lst = []
    while number > system-1:
        lst.insert(0, str(number%system))
        number = int(number/system)
    
    lst.insert(0, str(number))
    return lst

def from_system(str_num, system):
    str_len = len(str_num)
    res = 0
    i = 1
    d = {
        'a' : 10,
        'b' : 11,
        'c' : 12,
        'd' : 13,
        'e' : 14,
        'f' : 15,
    }
    while i <= str_len:
        if str_num[-i] in d:
            res += d[str_num[-i]] * system**(i-1)
        else:
            res += int(str_num[-i]) * system**(i-1)
        i += 1
    return res

def dec2bin(number):
    lst = to_system(int(number), 2)
    return ''.join(lst)
    
def dec2oct(number):
    lst = to_system(int(number), 8)
    return ''.join(lst)

def dec2hex(number):
    lst = to_system(int(number), 16)
    d = {
        '10' : 'a',
        '11' : 'b',
        '12' : 'c',
        '13' : 'd',
        '14' : 'e',
        '15' : 'f',
    }
    new_lst = []
    for i in lst:
        if i in d:
            new_lst.append(d[i])
        else:
            new_lst.append(i)

    return ''.join(new_lst)

def bin2dec(number):
    return from_system(number, 2)
    
def oct2dec(number):
    return from_system(number, 8)

def hex2dec(number):
    return from_system(number, 16)

