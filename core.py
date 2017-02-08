
import pickle
from os import stat
from datetime import datetime, timedelta


def main():
    """ None -> None
    Begins decision making and decides which path to follow.
    """
    while True:
        greet_answer = input("Enter the number 1 for a transaction; "
                             "to view inventory/transaction history, enter the number 2. "
                             "(enter the number 9 to exit at any time) ")
        # throughout the file, there are checks for the input of 9; these are the same as cancel
        if greet_answer == '1':
            print(choose_trans())
        elif greet_answer == '2':
            print(view_trans_or_inventory())
        elif greet_answer == '9':
            return 'Have a nice day!'
        else:
            print("I'm sorry, I didn't catch that.")


def choose_trans():
    """ (str) -> None
    Handles transaction choice.
    """
    choice = input("Please enter the number according to the transaction. "
                   "(rental - 1, purchase - 2, return - 3, or replace - 4) ").strip().lower()
    if choice == '1':
        item_num = input("Enter the corresponding number for your choice: \n"
                         "1 - Auger\n2 - Nailgun\n3 - Generator\n4 - Pressure Washer\n"
                         "5 - Air Compressor\n6 - Tilesaw").strip()
        time_choice = input(('Please enter 1 to rent the item for 5 hours, '
                             '2 for one day, 3 for one week, '
                             'and 4 for one month. ')).strip()
        return rent(choice_num_to_item(item_num), time_choice)
    elif choice == '2':
        item_num = input("Enter the corresponding number for your choice: \n"
                         "1 - Auger\n2 - Nailgun\n3 - Generator\n4 - Pressure Washer\n"
                         "5 - Air Compressor\n6 - Tilesaw").strip()
        return purchase(choice_num_to_item(item_num))
    elif choice == '3':
        item_id = input("Please input the ID of the returning item: ").strip().lower()

        damaged = input("Please enter 1 if the item is damaged and 2 if not: ")
        return return_item(item_id, damaged)
    elif choice == '4':
        item_id = input("Please input the ID of the item being replaced: ").strip().lower()
        return replace_item(item_id)
    elif choice == '9':
        return 'Have a nice day!'
    else:
        print("I'm sorry, I didn't quite catch that.")
        return


def rent(item: str, time_choice: str) -> str:
    """ (str) -> str
    Returns the overall total for renting <item> for <time_choice> amount of time,
    along with the date and time the tool should be returned by.

    >>> rent(auger)
    Tool ID: aug1
    Return By: 01/20/17 15:08
    Total Due: $80.25
    >>> rent(nailgun)
    Tool ID: nai3
    Return By: 02/08/17 13:53
    Total Due: $224.70
    """
    if check_inventory(item):
        list_for_history = []
        time_dict = {'1': {'time': '5hour', 'percent': .2},
                     '2': {'time': '1day', 'percent': .3},
                     '3': {'time': '1week', 'percent': .6},
                     '4': {'time': '1month', 'percent': .9}}
        date_due = calculate_return_date(time_dict[time_choice]['time'])
        price = get_price(item)
        amount_owed = ((price*.1)+(price*time_dict[time_choice]['percent']))*1.07
        item_id = update_inventory_remove(item)
        list_for_history.extend([item_id,
                                 'rental',
                                 'N/A', 'N/A',
                                 time_dict[time_choice]['time'],
                                 amount_owed,
                                 datetime.now(),
                                 date_due])
        update_trans_history(list_for_history)
        data_string = 'Tool ID: {0}\nReturn By: {1}\nTotal Due: ${2:.2f}'.format(
            item_id.upper(),
            date_due,
            amount_owed
        )
        return data_string
    elif item == '9':
        return 'Have a nice day!'
    else:
        return "I'm sorry, that item is currently unavailable. Please check again later."


def calculate_return_date(time_choice: str) -> datetime:
    """
    Returns a datetime object that is timechoice away from the current
    datetime.
    """
    time_conv_dict = {'5hour': 5,
                      '1day': 24,
                      '1week': 168,
                      '1month': 720}
    hours = time_conv_dict[time_choice]
    return_date = datetime.now() + timedelta(hours=hours)
    return return_date


def purchase(item):
    """ (str) -> str
    Returns the total and item id when given an item.
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
        pretty_str = 'Total: ${0:.2f}; Item ID: {1}'.format(price, current_id)
        return pretty_str
    elif item == '9':
        return 'Have a nice day!'
    else:
        print("I'm sorry, that item is currently unavailable. Please check again later.")
        return


def return_item(item_id, damaged):
    """ (str, str) -> str
    Returns the total when given a item_id. Also updates inventory and trans history.
    """
    if item_id == '9':
        return 'Have a nice day!'
    else:
        id_codes = {'nai': 'nailgun', 'aug': 'auger', 'gen': 'generator',
                    'air': 'air_compressor', 'til': 'tilesaw', 'pre': 'pressure_washer'}
        if item_id[:3] in id_codes:
            list_for_history = []
            damaged_dict = {'1': True, '2': False}
            price = get_price(item_id_to_item(item_id))
            amount_owed = 0
            late_info = is_late(item_id)
            if isinstance(late_info, str):
                return late_info
            if late_info[0]:
                overdue_charge = float(late_info[1]) * (price*.2)
                if overdue_charge > price:
                    overdue_charge = price
                amount_owed += overdue_charge
            if damaged_dict[damaged] is False:
                amount_owed -= .1*price
            amount_owed = amount_owed*1.07
            list_for_history.extend([item_id,
                                     'return',
                                     damaged_dict[damaged],
                                     late_info[0],
                                     'N/A',
                                     amount_owed,
                                     datetime.now(),
                                     'N/A'])
            update_trans_history(list_for_history)
            update_inventory_add(item_id)
            pretty_str = 'Total: ${0:.2f}'.format(amount_owed)
            return pretty_str
        else:
            print("That is an invalid ID. Please try again.")
            return


def replace_item(item_id):
    """ (str) -> str
    Returns the total owed when given a item_id. Also updates inventory and trans history.
    """
    if item_id == '9':
        return 'Have a nice day!'
    else:
        int(item_id[3:])
        id_codes = {'nai': 'nailgun', 'aug': 'auger', 'gen': 'generator',
                    'air': 'air_compressor', 'til': 'tilesaw', 'pre': 'pressure_washer'}
        if item_id[:3] in id_codes:
            item = item_id_to_item(item_id)
            list_for_history = []
            price = get_price(item)
            price = (price-(price*.1))*1.07
            current_date = datetime.today()
            list_for_history.extend([item_id,
                                     'replacement',
                                     'N/A', 'N/A',
                                     'N/A', price,
                                     current_date,
                                     'N/A'])
            update_trans_history(list_for_history)
            pretty_str = 'Total: ${0:.2f}'.format(price)
            return pretty_str
        else:
            print("That is an invalid ID. Please try again.")
            return


def is_late(item_id):
    """ (str) -> list(bool, float) or str
    Returns a list of a bool (if the item is late) and a float (how many hours overdue).
    Checks trans_history.p to see if the given item_id is late or not.
    """
    late = False
    with open("trans_history.p", 'rb') as fin:
        history = pickle.load(fin)
    for each in reversed(history):
        if each['item_id'] == item_id:
            # unorderable types? weird because theyre both datetime objects
            if each['date_due'] > datetime.now(): # if it's late
                hours = return_hours(datetime.now(), each['date_due'])
                late = True
                return [late, hours]
            else:
                hours = 0
                return [late, hours]
    return "I can't seem to find that item in the transaction history. Sorry!"


def choice_num_to_item(num: str) -> str:
    """
    Returns the correct item when given a number choice
    """
    num_to_item_dict = {'1': 'auger',
                        '2': 'nailgun',
                        '3': 'generator',
                        '4': 'pressure washer',
                        '5': 'air compressor',
                        '6': 'tilesaw'}
    return num_to_item_dict[num]


def return_hours(now, before_time):
    """ (datetime, datetime) -> float
    Returns the amount of hours between two datetime objects.
    """
    diff = now - before_time
    return diff.seconds//3600 + (diff.seconds//60)%60/60


def get_price(item):
    """ (str) -> int
    Returns the replacement price from inventory when given an item.
    """
    with open('inventory.p', 'rb') as fin:
        inv = pickle.load(fin)
    return int(inv[item]['price'])


def check_inventory(item):
    """ (str) -> bool
    Returns T/F whether or not an item is in stock by accessing inventory.p.
    """
    with open('inventory.p', 'rb') as fin:
        inv = pickle.load(fin)
    if inv[item]['num'] == 0:
        return False
    else:
        return True


def item_id_to_item(item_id):
    """ (str) -> str
    Returns the item associated to the given item_id.
    """
    id_codes = {'nai': 'nailgun', 'aug': 'auger', 'gen': 'generator',
                'air': 'air_compressor', 'til': 'tilesaw', 'pre': 'pressure_washer'}
    item = id_codes[item_id[:3]]
    return item


def view_trans_or_inventory():
    """ None -> None
    Prints inventory or transaction history to the terminal.
    """
    option_answer = input("Please enter 1 to view inventory and 2 to view transaction history. ")
    if option_answer == '1':
        with open('inventory.p', 'rb') as fin:
            if stat("inventory.p").st_size == 0:
                return "There's nothing here!"
            data = pickle.load(fin)
            data_string = ""
            for key, value in data.items():
                item = "Item - {0}; Price - ${1}; Number - {2}; IDs - {3}\n".format(
                    key.replace('_', ' ').capitalize(), value['price'], value['num'], value['ids'])
                data_string += item
            return data_string
    elif option_answer == '2':
        with open('trans_history.p', 'rb') as fin:
            if stat("trans_history.p").st_size == 0:
                return "There's nothing here!"
            data = pickle.load(fin)
            data_string = ""
            for each in data:
                if isinstance(each['date_due'], str):
                    trans = ("Item ID - "+each['item_id'].upper()+
                             "; Transaction - "+each['trans_type']+
                             "; Amount Charged - $"+str(each['amount_charged'])+"; "
                             "Time Choice - "+each['time_choice']+
                             "; Date Of - "+each['date_of_trans'].strftime('%m/%d/%Y %H:%M')+
                             "; Due By - "+each['date_due']+"; "
                             "Damaged on Return - "+each['return_info']['damaged']+
                             "; Past Due - "+each['return_info']['past_due']+"\n")
                else:
                    trans = ("Item ID - "+each['item_id'].upper()+
                             "; Transaction - "+each['trans_type']+
                             "; Amount Charged - $"+str(each['amount_charged'])+"; "
                             "Time Choice - "+each['time_choice']+
                             "; Date Of - "+each['date_of_trans'].strftime('%m/%d/%Y %H:%M')+
                             "; Due By - "+each['date_due'].strftime('%m/%d/%Y %H:%M')+"; "
                             "Damaged on Return - "+each['return_info']['damaged']+
                             "; Past Due - "+each['return_info']['past_due']+"\n")
                data_string += trans
            return data_string
    else:
        print("I'm sorry, I didn't quite get that.")
        view_trans_or_inventory()


def update_trans_history(list_of_info):
    """ (list) -> None
    Updates the list of dictionaries of transaction history objects in trans_history.p.
    The transaction history is stored as a list of dictionaries.
    """
    with open('trans_history.p', 'rb') as fin:
        # if the file is empty, make an empty list
        if stat("trans_history.p").st_size == 0:
            list_of_dict = []
        # if not, load up the current list
        else:
            list_of_dict = pickle.load(fin)
    with open('trans_history.p', 'wb') as fin:
        # converts the list_of_info to a dictionary and appends it
        list_of_dict.append({'item_id': list_of_info[0].lower(),
                             'trans_type': list_of_info[1],
                             'return_info': {'damaged': list_of_info[2],
                                             'past_due': list_of_info[3]},
                             'time_choice': list_of_info[4],
                             'amount_charged': list_of_info[5],
                             'date_of_trans': list_of_info[6],
                             'date_due': list_of_info[7]})
        pickle.dump(list_of_dict, fin)


def update_inventory_add(item_id):
    """ (str) -> None
    Updates inventory.p when something is being added back to the inventory.
    """
    # dictionary used to match item id to the item for easier lookup
    item = item_id_to_item(item_id)
    with open('inventory.p', 'rb') as fin:
        inv_dict = pickle.load(fin)
    needed_list = inv_dict[item]['ids']
    inv_dict[item]['num'] += 1
    needed_list.append(item_id)
    inv_dict[item]['ids'] = needed_list
    with open("inventory.p", 'wb') as fin:
        pickle.dump(inv_dict, fin)


def update_inventory_remove(item):
    """ (str) -> str
    Updates inventory.p when something is being removed from the inventory.
    """
    with open('inventory.p', 'rb') as fin:
        inv_dict = pickle.load(fin)
    needed_list = inv_dict[item]['ids']
    inv_dict[item]['num'] -= 1
    removed_item_id = needed_list.pop()
    # updates the list in the dictionary with the new list
    # (the list with the item_id removed)
    inv_dict[item]['ids'] = needed_list
    with open("inventory.p", 'wb') as fin:
        pickle.dump(inv_dict, fin)
    return removed_item_id


def wipe_trans_history():
    """ (None) -> None
    Deletes all content from trans_history.
    """
    fin = open('trans_history.p', 'wb')
    fin.close()


def initialize_inventory():
    """ None -> None
    Initializes inventory.p if it is empty. Inventory is stored as a
    dictionary of dictionaries.
    """
    # exact format of inventory, for reference
    tools = {'auger': {'price': 250,
                       'num': 2,
                       'ids': ['aug1', 'aug2']},
             'generator': {'price': 1500,
                           'num': 3,
                           'ids': ['gen1', 'gen2', 'gen3']},
             'nailgun': {'price': 300,
                         'num': 5,
                         'ids': ['nai1', 'nai2', 'nai3', 'nai4', 'nai5']},
             'air_compressor': {'price': 500,
                                'num': 3,
                                'ids': ['air1', 'air2', 'air3']},
             'tilesaw': {'price': 350,
                         'num': 1,
                         'ids': ['til1']},
             'pressure_washer': {'price': 600,
                                 'num': 2,
                                 'ids': ['pre1', 'pre2']}
            }
    with open('inventory.p', 'wb') as fin:
        pickle.dump(tools, fin)


if __name__ == '__main__':
    print(main())
