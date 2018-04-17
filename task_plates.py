plates = int(input())
detergent = float(input())

while plates > 0:
    detergent -= 0.5
    if detergent < 0:
        print('Моющее средство закончилось. Осталось',plates,'тарелок')
        break;
    plates -= 1

if not plates:
    if detergent:
        print('Все тарелки вымыты. Осталось',detergent,'ед. моющего средства')
    else:
        print('Все тарелки вымыты, моющее средство закончилось')
