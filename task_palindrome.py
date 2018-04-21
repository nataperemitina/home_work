def is_palindrome(s):
    
    string = str(s).lower()
   
    start = 0
    end = len(string) - 1

    while start < end:
        if string[start].isspace():
            start += 1
        elif string[end].isspace():
            end -= 1
        elif string[start] != string[end]:
            return False
        else:
            start += 1
            end -= 1

    return True

