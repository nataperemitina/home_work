def bubble_sort(lst):
    j = 1 # счетчик уже отсортированных элементов 
    count = len(lst) # количество элементов в списке
    '''
    Внешний цикл для прохода по списку count - 1 раз 
    (либо  до фиксирования момента, когда не понадобилось переставить ни одного элемента)
    В результате каждого прохода по внешнему циклу максимальный элемент из элементов с 0-го по count - j
    оказывается в позиции с индексом [count - j], минимальный элемент смещается на одну позицию в сторону уменьшения
    '''
    while j < count:

        f = False # флаг индикации произошедшей перестановки элементов
        i = 0 # индекс элемента для сравнения с соседним и перестановки в случае необходимости
        
        '''
        Внутренний цикл для прохода по еще не отсортированной части списка
        ''' 
        while i < (count - j):
            if lst[i] > lst[i+1]: # cравниваем текущий и следующий за ним элемент

                lst[i],lst[i+1] = lst[i+1],lst[i] # если текущий элемент больше, то меняем элементы местами
                f = True # выставляем флаг, что элементы были переставлены, значит список еще не отсортирован

            i += 1 # переходим к следующему элементу во внутреннем цикле

        if f == False: # если ни одной перестановки не было
            break # значит, список уже отсортирован, больше проходов не нужно
        
        j += 1 # увеличиваем счетчик отсортированных элементов

    return lst

