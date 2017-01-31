def main():
    """ None -> None
    Main function that runs all of the smaller functions.
    """
    begin_decisions()



def rent(item, time_choice):
    """ (str, str) -> str
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

def purchase(item):
    """ (str) -> str
    Returns the total when given an item.
    """


def return_item(item):
    """ (str) -> str
    Returns the total when given a item.
    """


def replace_item(item):
    """ (str) -> str
    Returns the total when given a item.
    """


def begin_decisions():
    """ None -> None
    Begins decision making and decides which path to follow.
    """
    print("Is this a transaction or would you like to view inventory/transaction history?")
    greet_answer = input()
    # begin decision making here
    if greet_answer == 'transaction':
        # start transaction stuff
        which_trans = input(
            "What kind of transaction will this be? (rental, purchase, return, or replace) ")
        if which_trans == 'rental':
            item = input("What item is in question? ")
            if check_inventory(item):
                time_choice = input(
                    '''
                    Please choose the length of time to rent a {0}.
                    (5hour, 1day, 1week, or 1month) ''')
                rent(item, time_choice)
            else:
                print("I'm sorry, that item is currently unavailable. Please check again later.")
                begin_decisions()
        elif which_trans == 'purchase':
            item = input("What item is in question? ")
            if check_inventory(item):
                purchase(item)
            else:
                print("I'm sorry, that item is currently unavailable. Please check again later.")
                begin_decisions()
        elif which_trans == 'return':
            item_id = input("Please input the ID of the returning item: ")
            return_item(item_id)
        elif which_trans == 'replace':
            item_id = input("Please input the ID of the item being replaced: ")
            replace_item(item_id)
        else:
            print("I'm sorry, I didn't quite catch that.")
        # add something here to repeat the question
    elif greet_answer == 'view inventory/transaction history':
        option_answer = input("Would you like to view current inventory or transaction history? ")
        if option_answer == 'inventory':
            with open('inventory.txt', 'r') as fin:
                print(fin.read())
        elif option_answer == 'transaction history':
            with open('transaction_history.txt') as fin:
                print(fin.read())
        else:
            print("I'm sorry, I didn't quite get that.")
            # add something here to repeat the question
    else:
        print("I'm sorry, I didn't catch that.")
        begin_decisions()


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

if __name__ == '__main__':
    main()
