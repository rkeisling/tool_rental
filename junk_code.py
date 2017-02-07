def main():
    some_in = input("Which option? ").strip().lower()
    while True:
        if some_in == 'a':
            func_a()
            break
        elif some_in == 'b':
            func_b()
            break
        elif some_in == 'c':
            func_c()
            break
        else:
            print("That's not an option.")
            return


def func_a():
    print("Blah, blahhhhhhh.")
    a = 2
    a += 25
    return func_b()


def func_b():
    print('This is B.')
    b = 44
    return func_c()


def func_c():
    print("Hello, C here!")
    c = 'apple'
    return


if __name__ == '__main__':
    main()
