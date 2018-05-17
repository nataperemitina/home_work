def get_free_land(tpl1, tpl2):
    if not tpl1[0]:
        raise ValueError('Не задана площадь участка')

    S = tpl1[0] * 100
    s = tpl2[0] * tpl2[1]

    if not s:
        raise ValueError('Не задана площадь грядки')

    if s > S:
        raise ValueError('Размер грядки больше размера участка')

    return S % s
