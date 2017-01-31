

def main():
    """ None -> None
    Begins decision making and decides which path to follow.
    """
    print("Is this a transaction or would you like to view inventory/transaction history?")
    greet_answer = input()
    # begin decision making here
    if greet_answer == 'transaction':
        # start transaction stuff
        choose_trans()
    elif greet_answer == 'view inventory/transaction history':
        view_trans_or_inventory()
    elif greet_answer == 'cancel':
        return 'Have a nice day!'
    else:
        print("I'm sorry, I didn't catch that.")
        main()


def choose_trans():
    """ (str) -> None
    Handles transaction choice.
    """
    choice = input(
        "What kind of transaction will this be? (rental, purchase, return, or replace) ")
    if choice == 'rental':
        item = input("What item is in question? ").strip().lower().capitalize()
        rent(item)
    elif choice == 'purchase':
        item = input("What item is in question? ")
        purchase(item)
    elif choice == 'return':
        item_id = input("Please input the ID of the returning item: ")
        return_item(item_id)
    elif choice == 'replace':
        item_id = input("Please input the ID of the item being replaced: ")
        replace_item(item_id)
    else:
        print("I'm sorry, I didn't quite catch that.")
        main()


def rent(item):
    """ (str) -> str
    Returns the overall total for renting <item> for <time_choice> amount of time,
    along with the date and time the tool should be returned by.

    >>> rent(Auger, AUG1, 5hour, 01/20/17 10:08)
    Tool ID: AUG1
    Return By: 01/20/17 15:08
    Total Due: $80.25
    >>> rent(Nailgun, NAI3, 1week, 02/01/17 13:53)
    Tool ID: NAI3
    Return By: 02/08/17 13:53
    Total Due: $224.7
    """
    if check_inventory(item):
        time_choice = input(
            '''
            Please choose the length of time to rent a {0}.
            (5hour, 1day, 1week, or 1month) ''').format(item)
        return (item, time_choice)
    else:
        print("I'm sorry, that item is currently unavailable. Please check again later.")
        main()


def purchase(item):
    """ (str) -> str
    Returns the total when given an item.
    """
    if check_inventory(item):
        # continue code here
        return item
    else:
        print("I'm sorry, that item is currently unavailable. Please check again later.")
        main()


def return_item(item):
    """ (str) -> str
    Returns the total when given a item.
    """
    return item


def replace_item(item):
    """ (str) -> str
    Returns the total when given a item.
    """
    return item


def check_inventory(item):
    """ (str) -> bool
    Returns T/F whether or not an item is in stock by accessing inventory.txt.
    """
    with open('inventory.txt') as file:
        inv = file.readlines()
    formatted_inv = [each.strip().split(' - ') for each in inv]
    for each in formatted_inv:
        if item == each[0]:
            if len(each[3]) == 0:
                return False
            else:
                return True


def view_trans_or_inventory():
    """ None -> None
    Prints inventory or transaction history to the terminal.
    """
    option_answer = input("Would you like to view current inventory or transaction history? ")
    if option_answer == 'inventory':
        with open('inventory.txt', 'r') as fin:
            print(fin.read())
    elif option_answer == 'transaction history':
        with open('transaction_history.txt') as fin:
            print(fin.read())
    else:
        print("I'm sorry, I didn't quite get that.")
        view_trans_or_inventory()


if __name__ == '__main__':
    main()
