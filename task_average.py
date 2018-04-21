def average(lst):
    summa = 0
    for i in lst:
        summa += i
    
    return round(summa/len(lst), 3)

