import json
from os import stat


def main():
    """ None -> None
    Begins decision making and decides which path to follow.
    """
    print("Is this a transaction or would you "
          "like to view inventory/transaction history? "
          "(enter 'cancel' to exit at any time)")
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
        print(main())


def choose_trans():
    """ (str) -> None
    Handles transaction choice.
    """
    choice = input("What kind of transaction will this be? "
                   "(rental, purchase, return, or replace) ").strip().lower()
    if choice == 'rental':
        item = input("What item is in question? ").strip().lower().capitalize()
        print(rent(item))
    elif choice == 'purchase':
        item = input("What item is in question? ").strip().lower().capitalize()
        print(purchase(item))
    elif choice == 'return':
        item_id = input("Please input the ID of the returning item: ").strip()
        print(return_item(item_id))
    elif choice == 'replace':
        item_id = input("Please input the ID of the item being replaced: ").strip()
        print(replace_item(item_id))
    elif choice == 'cancel':
        return 'Have a nice day!'
    else:
        print("I'm sorry, I didn't quite catch that.")
        print(main())


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
    # needs to build up a string that eventually gets written to trans history
    # needs to remove said item id from inventory using update inventory
    # needs to calculate total owed amount and return it
    if check_inventory(item):
        time_choice = input(('Please choose the length of time to rent a '+item+'. '
                             '(5hour, 1day, 1week, or 1month) '))
        return (item, time_choice)
    elif item == 'cancel':
        return 'Have a nice day!'
    else:
        print("I'm sorry, that item is currently unavailable. Please check again later.")
        print(main())


def purchase(item):
    """ (str) -> str
    Returns the total when given an item.
    """
    # needs to use check_inventory, then grab an id from the available ones
    # in inventory
    # needs to build up a string that eventually gets written to trans history
    # needs to remove said item id from inventory using update_inventory
    # needs to calculate total owed amount and return it
    if check_inventory(item):
        # continue code here
        return item
    elif item == 'cancel':
        return 'Have a nice day!'
    else:
        print("I'm sorry, that item is currently unavailable. Please check again later.")
        main()


def return_item(item_id):
    """ (str) -> str
    Returns the total when given a item_id. Also updates inventory and trans history.
    """
    # needs to check and see if the item is late or not
    # if late, charge 20% of item value for every hour late
    # if more than item value, just charge item value minus 10% for deposit
    # needs to see if item is damaged
    # if damaged, charge nothing
    # if not damaged, refund deposit (10% of replacement value)
    # use update_inventory to put item_id back into appropriate list
    return item_id


def replace_item(item_id):
    """ (str) -> str
    Returns the total when given a item_id. Also updates inventory and trans history.
    """
    # works same way as purchase, but with specific id instead of generic item
    # replacement price is replacement price in inventory but minus 10% for deposit
    return item_id


def check_inventory(item):
    """ (str) -> bool
    Returns T/F whether or not an item is in stock by accessing inventory.json.
    """
    # needs to be reformatted for json files
    with open('inventory.json') as file:
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
    # need to change format of trans_history to json
    # cant just read json file, must format from whatever structure, probably
    # a list or dictionary
    option_answer = input("Would you like to view current inventory or transaction history? ")
    if option_answer == 'inventory':
        with open('inventory.json', 'r') as fin:
            print(fin.read())
    elif option_answer == 'transaction history':
        with open('trans_history.json') as fin:
            print(fin.read())
    else:
        print("I'm sorry, I didn't quite get that.")
        view_trans_or_inventory()


def update_trans_history(list_of_info):
    """ (list) -> None
    Updates the list of dictionaries of transaction history objects in trans_history.json.
    """
    with open('trans_history.json', 'r') as fin:
        if stat("trans_history.json").st_size == 0:
            list_of_dict = []
        else:
            list_of_dict = json.load(fin)
    with open('trans_history.json', 'w') as fin:
        list_of_dict.append({'item_id': list_of_info[0],
                             'trans_type': list_of_info[1],
                             'return_info': {'damaged': list_of_info[2],
                                             'past_due': list_of_info[3]},
                             'time_choice': list_of_info[4],
                             'amount_charged': list_of_info[5],
                             'date_of_trans': list_of_info[6],
                             'date_due': list_of_info[7]})
        json.dump(list_of_dict, fin)


def update_inventory(item_id):
    """ (str) -> None or str
    Updates inventory.json. If given an item id, it will add the item back to the
    inventory. If given the integer 0, it will return an item id and remove it
    from the inventory list as well as update the number in inventory.
    """
    id_codes = {'nai': 'nailgun', 'aug': 'auger', 'gen': 'generator',
                'air': 'air compressor', 'til': 'tile saw', 'pre': 'pressure washer'}
    item = id_codes[item_id[:3]]
    with open('inventory.json', 'r') as fin:
        inv_dict = json.load(fin)
    needed_list = inv_dict[item]['ids']
    if item_id == 0:
        inv_dict[item]['num'] -= 1
        item_id = needed_list.pop()
        inv_dict[item]['ids'] = needed_list
        with open("inventory.json", 'w') as fin:
            json.dump(inv_dict, fin)
        return item_id
    else:
        inv_dict[item]['num'] += 1
        needed_list.append(item_id)
        inv_dict[item]['ids'] = needed_list
        with open("inventory.json", 'w') as fin:
            json.dump(inv_dict, fin)


def initialize_inventory():
    """ None -> None
    Initializes inventory.json if it is empty.
    """
    tools = {'auger': {'price': 250,
                       'num': 2,
                       'ids': ['AUG1', 'AUG2']},
             'generator': {'price': 1500,
                           'num': 3,
                           'ids': ['GEN1', 'GEN2', 'GEN3']},
             'nailgun': {'price': 300,
                         'num': 5,
                         'ids': ['NAI1', 'NAI2', 'NAI3', 'NAI4', 'NAI5']},
             'aircompressor': {'price': 500,
                               'num': 3,
                               'ids': ['AIR1', 'AIR2', 'AIR3']},
             'tilesaw': {'price': 350,
                         'num': 1,
                         'ids': ['TIL1']},
             'pressurewasher': {'price': 600,
                                'num': 2,
                                'ids': ['PRE1', 'PRE2']}
            }
    with open('inventory.json', 'w') as fin:
        json.dump(tools, fin)


if __name__ == '__main__':
    print(main())
