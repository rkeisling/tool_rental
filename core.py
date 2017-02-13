'''
Module documentation here.
'''
import pickle
from os import stat
from datetime import datetime, timedelta
from collections import namedtuple
from typing import Union

TimePercent = namedtuple("TimePercent", ['time',
                                         'percent'])
TransInfo = namedtuple("TransInfo", ['item_id',
                                     'trans_type',
                                     'damaged',
                                     'past_due',
                                     'time_choice',
                                     'amount_charged',
                                     'date_of_trans',
                                     'date_due'])
LateInfo = namedtuple("LateInfo", ['late_bool',
                                   'hours'])
TransTypeAndId = namedtuple('TransTypeAndId', ['id',
                                               'trans_type'])


def rent(item: str, time_choice: str) -> str:
    """
    Returns the overall total for renting <item> for <time_choice> amount of time,
    along with the date and time the tool should be returned by.

    >>> rent('auger', '1week')
    Item ID: AUG1
    Return By: 01/20/17 15:08
    Total Due: $187.25
    >>> rent(nailgun, '1day')
    Item ID: NAI3
    Return By: 02/08/17 13:53
    Total Due: $128.40
    """
    if item == '9':
        return '\nHave a nice day!'
    elif is_valid_item(item) and check_inventory(item) and int(time_choice) <= 4:
        time_dict = {'1': TimePercent('5hour', .2),
                     '2': TimePercent('1day', .3),
                     '3': TimePercent('1week', .6),
                     '4': TimePercent('1month', .9)}
        date_due = calculate_return_date(time_dict[time_choice].time)
        price = get_price(item)
        amount_owed = ((price*.1)+(price*time_dict[time_choice].percent))*1.07
        item_id = update_inv_rem(item)
        trans_info = TransInfo(item_id,
                               'rental',
                               'N/A', 'N/A',
                               time_dict[time_choice].time,
                               amount_owed,
                               datetime.now(),
                               date_due)
        update_trans_history(trans_info)
        data_string = '\nItem ID: {0}\nReturn By: {1}\nTotal Due: ${2:.2f}'.format(
            item_id.upper(),
            date_due.strftime('%m/%d/%Y %H:%M'),
            amount_owed
        )
        return data_string
    else:
        return "\nI'm sorry, that item is currently unavailable. Please check again later."


def purchase(item: str) -> str:
    """
    Returns the total and item id in a string when given an item.
    """
    if item == '9':
        return '\nHave a nice day!'
    elif is_valid_item(item) and check_inventory(item):
        current_id = update_inv_rem(item).upper()
        price = get_price(item)*1.07
        current_date = datetime.today()
        trans_info = TransInfo(current_id,
                               'purchase',
                               'N/A', 'N/A',
                               'N/A', price,
                               current_date,
                               'N/A')
        update_trans_history(trans_info)
        pretty_str = '\nTotal: ${0:.2f}\nItem ID: {1}'.format(price, current_id)
        return pretty_str
    else:
        return "\nI'm sorry, that item is currently unavailable. Please check again later."


def return_item(item_id: str, damaged: bool) -> str:
    """
    Returns the total when given a item_id. Also updates inventory and trans history.
    """
    if item_id == '9':
        return '\nHave a nice day!'
    elif is_valid_item(item_id_to_item(item_id)):
        price = get_price(item_id_to_item(item_id))
        amount_owed = 0.0
        late_info = is_late(item_id)
        if isinstance(late_info, str):
            return late_info
        if late_info.late_bool:
            overdue_charge = float(late_info.hours) * (price*.2)
            if overdue_charge > price:
                overdue_charge = price
            amount_owed += overdue_charge
        if damaged is False:
            amount_owed -= .1*price
        trans_info = TransInfo(item_id,
                               'return',
                               damaged,
                               late_info.late_bool,
                               'N/A',
                               amount_owed,
                               datetime.now(),
                               'N/A')
        update_trans_history(trans_info)
        update_inv_add(item_id)
        pretty_str = '\nTotal: ${0:.2f}'.format(amount_owed)
        return pretty_str
    else:
        return "\nThat is an invalid ID. Please try again."


def replace_item(item_id: str) -> str:
    """
    Returns the total owed when given a item_id. Also updates inventory and trans history.
    """
    if item_id == '9':
        return '\nHave a nice day!'
    elif is_valid_item(item_id_to_item(item_id)):
        int(item_id[3:])
        id_codes = {'nai': 'nailgun', 'aug': 'auger', 'gen': 'generator',
                    'air': 'air_compressor', 'til': 'tilesaw', 'pre': 'pressure_washer'}
        if item_id[:3] in id_codes:
            item = item_id_to_item(item_id)
            price = float(get_price(item))
            price = (price-(price*.1))*1.07
            current_date = datetime.today()
            trans_info = TransInfo(item_id,
                                   'replacement',
                                   'N/A', 'N/A',
                                   'N/A', price,
                                   current_date,
                                   'N/A')
            update_trans_history(trans_info)
            pretty_str = '\nTotal: ${0:.2f}'.format(price)
            return pretty_str
    else:
        return "\nThat is an invalid ID. Please try again."


def is_valid_item(item: str) -> bool:
    """
    Returns whether or not an item is valid.
    """
    with open('inventory.p', 'rb') as fin:
        inv = pickle.load(fin)
    if item in inv:
        return True
    else:
        return False


def is_late(item_id: str) -> Union[LateInfo, str]:
    """
    Returns a list of a bool (if the item is late) and a float (how many hours overdue).
    Checks trans_history.p to see if the given item_id is late or not.
    """
    late = False
    trans_type_list = [] # type: List[TransTypeAndId]
    with open("trans_history.p", 'rb') as fin:
        history = pickle.load(fin)
    for each in reversed(history):
        trans_type_list.append(TransTypeAndId(each['item_id'], each['trans_type']))
        if each['item_id'] == item_id and each['trans_type'] == 'rental':
            for trans_id in trans_type_list:
                if trans_id.id == each['item_id'] and trans_id.trans_type == 'replacement':
                    return "\nI can't seem to find that item in the transaction history. Sorry!"
            if each['date_due'] < datetime.now(): # if it's late
                hours = get_time_diff(datetime.now(), each['date_due'])
                late = True
                return LateInfo(late, hours)
            else:
                hours = 0
                return LateInfo(late, hours)
    return "\nI can't seem to find that item in the transaction history. Sorry!"


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


def choice_num_to_item(num: str) -> str:
    """
    Returns the correct item when given a number choice
    """
    if int(num) <= 6:
        num_to_item_dict = {'1': 'auger',
                            '2': 'nailgun',
                            '3': 'generator',
                            '4': 'pressure_washer',
                            '5': 'air_compressor',
                            '6': 'tilesaw'}
        return num_to_item_dict[num]
    else:
        return '\nThat is not a valid choice.'


def get_time_diff(now: datetime, before_time: datetime) -> float:
    """
    Returns the amount of hours between two datetime objects.
    """
    return float("{0:.2f}".format(return_hours(now - before_time)))


def return_hours(diff: timedelta) -> int:
    """
    Converts a timedelta object into hours and returns it.
    """
    return round(diff.total_seconds()/3600)


def get_price(item: str) -> int:
    """
    Returns the replacement price from inventory when given an item.
    """
    with open('inventory.p', 'rb') as fin:
        inv = pickle.load(fin)
    return int(inv[item]['price'])


def check_inventory(item: str) -> bool:
    """
    Returns T/F whether or not an item is in stock by accessing inventory.p.
    """
    with open('inventory.p', 'rb') as fin:
        inv = pickle.load(fin)
    if inv[item]['num'] == 0:
        return False
    else:
        return True


def item_id_to_item(item_id: str) -> str:
    """
    Returns the item associated to the given item_id.
    """
    id_codes = {'nai': 'nailgun', 'aug': 'auger', 'gen': 'generator',
                'air': 'air_compressor', 'til': 'tilesaw', 'pre': 'pressure_washer'}
    if item_id[:3] in id_codes:
        item = id_codes[item_id[:3]]
        return item
    else:
        return '\nThat is an invalid ID. Please try again.'


def update_trans_history(trans_info_tuple: TransInfo) -> None:
    """
    Updates the list of dictionaries of transaction history objects in trans_history.p.
    The transaction history is stored as a list of dictionaries.
    """
    with open('trans_history.p', 'rb') as fin:
        # if the file is empty, make an empty list
        if stat("trans_history.p").st_size == 0:
            list_of_dict = [] # type: List[Dict]
        # if not, load up the current list
        else:
            list_of_dict = pickle.load(fin)
    with open('trans_history.p', 'wb') as fin:
        list_of_dict.append({'item_id': trans_info_tuple.item_id.lower(),
                             'trans_type': trans_info_tuple.trans_type,
                             'return_info': {'damaged': trans_info_tuple.damaged,
                                             'past_due': trans_info_tuple.past_due},
                             'time_choice': trans_info_tuple.time_choice,
                             'amount_charged': trans_info_tuple.amount_charged,
                             'date_of_trans': trans_info_tuple.date_of_trans,
                             'date_due': trans_info_tuple.date_due})
        pickle.dump(list_of_dict, fin)


def update_inv_add(item_id: str) -> None:
    """
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


def update_inv_rem(item: str) -> str:
    """
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


def wipe_trans_history() -> str:
    """
    Deletes all content from trans_history.
    """
    fin = open('trans_history.p', 'wb')
    fin.close()
    return '\nThe transaction history has been wiped.'


def initialize_inventory() -> str:
    """
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
    return '\nThe inventory has been initialized.'
