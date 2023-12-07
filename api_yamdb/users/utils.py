def my_max_length(data):
    '''
    Функция вычисляет количество символов в
    самом длинном слове.
    '''
    mylist = [tup[0] for tup in data]
    return (max([len(i) for i in mylist]))
