from datetime import datetime, timedelta

def counter():
    now = datetime.now()
    new_year = datetime(now.year+1, 1, 1)
    
    delta = new_year - now

    days = delta.days
    hours = int(delta.seconds/3600)
    minutes = int((delta.seconds % 3600)/60)

    def names(num, lst):
        str_num = str(num)
        num_len = len(str_num)
        units = int(str_num[num_len - 1])
        
        if units == 1:
            return str_num + ' ' + lst[0]
            
        if units in range(2, 5) and (num_len < 2 or str_num[num_len - 2] != '1'):
            return str_num + ' ' + lst[1]
        
        return str_num + ' ' + lst[2]
    
    return names(days,['день','дня','дней'])+' '+names(hours,['час','часа','часов'])+' '+names(minutes,['минута','минуты','минут']) 


