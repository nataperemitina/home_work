def encode(text, offset=0):
    i = 0
    l = len(text)
    lst = []
    alpha_count = 26

    max_upper = ord('Z')
    max_lower = ord('z')

    while i < l:
        if not text[i].isalpha():
            lst.append(text[i])
        else:
            new_ord = ord(text[i]) + offset
            if text[i].isupper():
                if new_ord > max_upper:
                    new_ord -= alpha_count
            elif new_ord > max_lower:
                new_ord -= alpha_count
            lst.append(chr(new_ord))
        i += 1

    return ''.join(lst)

def decode(text, offset=0):
    i = 0
    l = len(text)
    lst = []
    alpha_count = 26

    min_upper = ord('A')
    min_lower = ord('a')

    while i < l:
        if not text[i].isalpha():
            lst.append(text[i])
        else:
            new_ord = ord(text[i]) - offset
            if text[i].isupper():
                if new_ord < min_upper:
                    new_ord += alpha_count
            elif new_ord < min_lower:
                new_ord += alpha_count
            lst.append(chr(new_ord))
        i += 1

    return ''.join(lst)

