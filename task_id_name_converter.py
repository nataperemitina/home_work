def camel_to_snake(name):
    lst = []
    i = 1
    prev = 1
    l = len(name)
    while i <= l:
        if name[-i].isupper():
            if prev == 1:
                lst.insert(0, name[-i:].lower())
            else: 
                lst.insert(0, name[-i:-prev].lower())
            prev = i
            
        i += 1
    
    if prev != l:
        lst.insert(0, name[:-prev])

    return '_'.join(lst)

def snake_to_camel(name):
    lst = name.split('_')
    name = ''
    for word in lst:
        name = name + word.capitalize()

    return name
    

