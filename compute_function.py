def func(startNumber: int):
    """
    Function that takes one Integer argument and giving result array of 3x+1 loop

    :param startNumber: Integer starting value
    :return: Tuple formed from List of calculated values and Integer number of steps
    """

    array = [startNumber]
    i = 0
    # flaga = False OLD SYSTEM
    while not (array[-1] == 1 or array[-1] == -1 or array[-1] == -5 or array[-1] == -25 or array[-1] == 0):
        if array[i] % 2 == 0:
            array.append(array[i]/2)
        else:
            array.append(3*array[i]+1)
        i+=1
        # if i > 200 and flaga == False: OLD SYSTEM
            # input("Wartość przekroczyła 200 kroków -> Wciśnij dowolny klawisz...") OLD SYSTEM
            # flaga = True OLD SYSTEM
    return array, i+1