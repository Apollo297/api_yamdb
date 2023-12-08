def my_max_length(data):
    '''
    Функция вычисляет количество символов в
    самом длинном слове.
    '''
    mylist = [i for i, _ in data]
    return (
        max(
            [len(i) for i in mylist]
        )
    )
