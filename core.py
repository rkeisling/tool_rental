import json
from os import stat
from datetime import datetime


def main():
    """ None -> None
    Begins decision making and decides which path to follow.
    """
    print("Enter the number 1 for a transaction; "
          "to view inventory/transaction history, enter the number 2. "
          "(enter the number 9 to exit at any time)")
    greet_answer = input()
    # begin decision making here
    if greet_answer == '1':
        # start transaction stuff
        return choose_trans()
    elif greet_answer == '2':
        return view_trans_or_inventory()
    elif greet_answer == '9':
        return 'Have a nice day!'
    else:
        print("I'm sorry, I didn't catch that.")
        return main()


def choose_trans():
    """ (str) -> None
    Handles transaction choice.
    """
    choice = input("Please enter the number according to the transaction. "
                   "(rental - 1, purchase - 2, return - 3, or replace - 4) ").strip().lower()
    if choice == '1':
        item = input("What item is in question? ").strip().lower()
        return rent(item)
    elif choice == '2':
        item = input("What item is in question? ").strip().lower()
        return purchase(item)
    elif choice == '3':
        item_id = input("Please input the ID of the returning item: ").strip()
        return return_item(item_id)
    elif choice == '4':
        item_id = input("Please input the ID of the item being replaced: ").strip()
        return replace_item(item_id)
    elif choice == '9':
        return 'Have a nice day!'
    else:
        print("I'm sorry, I didn't quite catch that.")
        return main()


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
    elif item == '9':
        return 'Have a nice day!'
    else:
        print("I'm sorry, that item is currently unavailable. Please check again later.")
        print(main())


def purchase(item):
    """ (str) -> str
    Returns the total when given an item.
    """
    list_for_history = []
    if check_inventory(item):
        current_id = update_inventory_remove(item)
        price = get_price(item)*1.07
        current_date = datetime.today()
        list_for_history.extend([current_id,
                                 'purchase',
                                 'N/A', 'N/A',
                                 'N/A', price,
                                 current_date,
                                 'N/A'])
        update_trans_history(list_for_history)
        pretty_str = 'Total: {0}; Item ID: {1}'.format(price, current_id)
        return pretty_str
    elif item == '9':
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


def get_price(item):
    """ (str) -> int
    Returns the replacement price from inventory when given an item.
    """
    with open('inventory.json') as fin:
        inv = json.load(fin)
    return int(inv[item]['price'])


def check_inventory(item):
    """ (str) -> bool
    Returns T/F whether or not an item is in stock by accessing inventory.json.
    """
    with open('inventory.json') as fin:
        inv = json.load(fin)
    if inv[item]['num'] == 0:
        return False
    else:
        return True


def view_trans_or_inventory():
    """ None -> None
    Prints inventory or transaction history to the terminal.
    """
    option_answer = input("Please enter 1 to view inventory and 2 to view transaction history. ")
    if option_answer == '1':
        with open('inventory.json', 'r') as fin:
            data = json.load(fin)
            data_string = ""
            for key, value in data.items():
                item = "Item - {0}; Price - ${1}; Number - {2}; IDs - {3}\n".format(
                    key.replace('_', ' ').capitalize(), value['price'], value['num'], value['ids'])
                data_string += item
            return data_string
    elif option_answer == '2':
        with open('trans_history.json') as fin:
            data = json.load(fin)
            data_string = ""
            for each in data:
                trans = ("Item ID - "+each['item_id']+
                         "; Transaction - "+each['trans_type']+
                         "; Amount Charged - $"+str(each['amount_charged'])+"; "
                         "Time Choice - "+each['time_choice']+
                         "; Date Of - "+each['date_of_trans']+
                         "; Due By - "+each['date_due']+"; "
                         "Damaged on Return - "+each['return_info']['damaged']+
                         "; Past Due - "+each['return_info']['past_due']+"\n")
                data_string += trans
            return data_string
    else:
        print("I'm sorry, I didn't quite get that.")
        view_trans_or_inventory()


def update_trans_history(list_of_info):
    """ (list) -> None
    Updates the list of dictionaries of transaction history objects in trans_history.json.
    The transaction history is stored as a list of dictionaries.
    """
    with open('trans_history.json', 'r') as fin:
        # if the file is empty, make an empty list
        if stat("trans_history.json").st_size == 0:
            list_of_dict = []
        # if not, load up the current list
        else:
            list_of_dict = json.load(fin)
    with open('trans_history.json', 'w') as fin:
        # converts the list_of_info to a dictionary and appends it
        list_of_dict.append({'item_id': list_of_info[0],
                             'trans_type': list_of_info[1],
                             'return_info': {'damaged': list_of_info[2],
                                             'past_due': list_of_info[3]},
                             'time_choice': list_of_info[4],
                             'amount_charged': list_of_info[5],
                             'date_of_trans': list_of_info[6],
                             'date_due': list_of_info[7]})
        json.dump(list_of_dict, fin, default=json_serial)


def update_inventory_add(item_id):
    """ (str) -> None
    Updates inventory.json when something is being added back to the inventory.
    """
    # dictionary used to match item id to the item for easier lookup
    id_codes = {'nai': 'nailgun', 'aug': 'auger', 'gen': 'generator',
                'air': 'air compressor', 'til': 'tile saw', 'pre': 'pressure washer'}
    item = id_codes[item_id[:3]]
    with open('inventory.json', 'r') as fin:
        inv_dict = json.load(fin)
    needed_list = inv_dict[item]['ids']
    inv_dict[item]['num'] += 1
    needed_list.append(item_id)
    inv_dict[item]['ids'] = needed_list
    with open("inventory.json", 'w') as fin:
        json.dump(inv_dict, fin)


def update_inventory_remove(item):
    """ (str) -> str
    Updates inventory.json when something is being removed from the inventory.
    """
    with open('inventory.json', 'r') as fin:
        inv_dict = json.load(fin)
    needed_list = inv_dict[item]['ids']
    inv_dict[item]['num'] -= 1
    removed_item_id = needed_list.pop()
    # updates the list in the dictionary with the new list
    # (the list with the item_id removed)
    inv_dict[item]['ids'] = needed_list
    with open("inventory.json", 'w') as fin:
        json.dump(inv_dict, fin)
    return removed_item_id


def initialize_inventory():
    """ None -> None
    Initializes inventory.json if it is empty. Inventory is stored as a
    dictionary of dictionaries.
    """
    # exact format of inventory, for reference
    tools = {'auger': {'price': 250,
                       'num': 2,
                       'ids': ['AUG1', 'AUG2']},
             'generator': {'price': 1500,
                           'num': 3,
                           'ids': ['GEN1', 'GEN2', 'GEN3']},
             'nailgun': {'price': 300,
                         'num': 5,
                         'ids': ['NAI1', 'NAI2', 'NAI3', 'NAI4', 'NAI5']},
             'air_compressor': {'price': 500,
                                'num': 3,
                                'ids': ['AIR1', 'AIR2', 'AIR3']},
             'tilesaw': {'price': 350,
                         'num': 1,
                         'ids': ['TIL1']},
             'pressure_washer': {'price': 600,
                                 'num': 2,
                                 'ids': ['PRE1', 'PRE2']}
            }
    with open('inventory.json', 'w') as fin:
        json.dump(tools, fin)


def json_serial(obj):
    """ (obj) -> None
    JSON serializer for objects not serializable by default json code
    """
    # this function fixes an issue with json serialization of datetime objects
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")


if __name__ == '__main__':
    print(main())
