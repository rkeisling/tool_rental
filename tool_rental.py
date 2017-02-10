"""These are all the top level interactions for core."""
import pickle
from os import stat
from typing import Any
from core import (wipe_trans_history,
                  initialize_inventory,
                  rent,
                  purchase,
                  return_item,
                  replace_item,
                  choice_num_to_item,
                  is_valid_item)

def main() -> Any:
    """
    Main function; takes the the majority of the inputs and ties the program together.
    """
    while True:
        greet_answer = input("Enter the number 1 for a transaction.\n"
                             "To view inventory/transaction history, enter 2.\n"
                             "To wipe the transaction history or "
                             "initialize the inventory, enter 3.\n"
                             "To view total revenue, enter 4.\n"
                             "Enter the number 9 to exit at any time.\n")
        # throughout the file, there are checks for the input of 9; these are the same as cancel
        if greet_answer == '1':
            print(choose_trans())
        elif greet_answer == '2':
            option_answer = input(
                "\nPlease enter 1 to view inventory and 2 to view transaction history. ")
            print(view_trans_or_inventory(option_answer))
        elif greet_answer == '3':
            choice = input(('\nEnter 1 to wipe the transaction history.\n'
                            'Enter 2 to initialize the inventory.\n'
                            'Enter 3 to do both.\n'))
            if choice == '1':
                print(wipe_trans_history())
            elif choice == '2':
                print(initialize_inventory())
            elif choice == '3':
                print(wipe_trans_history())
                print(initialize_inventory())
            elif choice == '9':
                return '\nHave a nice day!'
            else:
                print("\nI'm sorry, I didn't catch that.")
        elif greet_answer == '4':
            print(view_total_revenue())
        elif greet_answer == '9':
            return '\nHave a nice day!'
        else:
            print("\nI'm sorry, I didn't catch that.")


def choose_trans() -> Any:
    """
    Handles transaction choice; returns result of one of several functions.
    """
    choice = input("\nPlease enter the number according to the transaction.\n"
                   "1 - Rental\n2 - Purchase\n3 - Return\n4 - Replace\n").strip().lower()
    if choice == '1':
        item_num = input("\nEnter the corresponding number for your choice: \n"
                         "1 - Auger\n2 - Nailgun\n3 - Generator\n4 - Pressure Washer\n"
                         "5 - Air Compressor\n6 - Tilesaw\n").strip()
        time_choice = input(('\nEnter 1 to rent the item for 5 hours.\n'
                             'Enter 2 for one day.\nEnter 3 for one week.\n'
                             'Enter 4 for one month.\n')).strip()
        if is_valid_item(choice_num_to_item(item_num)):
            return rent(choice_num_to_item(item_num), time_choice)
    elif choice == '2':
        item_num = input("\nEnter the corresponding number for your choice: \n"
                         "1 - Auger\n2 - Nailgun\n3 - Generator\n4 - Pressure Washer\n"
                         "5 - Air Compressor\n6 - Tilesaw\n").strip()
        if is_valid_item(choice_num_to_item(item_num)):
            return purchase(choice_num_to_item(item_num))
    elif choice == '3':
        item_id = input("\nPlease input the ID of the returning item.\n").strip().lower()

        damaged = input("\nPlease enter 1 if the item is damaged and 2 if not.\n")
        damaged_dict = {'1': True, '2': False}
        return return_item(item_id, damaged_dict[damaged])
    elif choice == '4':
        item_id = input("\nPlease input the ID of the item being replaced.\n").strip().lower()
        return replace_item(item_id)
    elif choice == '9':
        return '\nHave a nice day!'
    else:
        return "\nI'm sorry, I didn't quite catch that."


def view_trans_or_inventory(option_answer: str) -> str:
    """
    Prints inventory or transaction history to the terminal.
    """
    if option_answer == '1':
        with open('inventory.p', 'rb') as fin:
            if stat("inventory.p").st_size == 0:
                return "There's nothing here!"
            data = pickle.load(fin)
            data_string = ""
            for key, value in data.items():
                item = "Item - {0}\nPrice - ${1}\nNumber - {2}\nIDs - {3}\n--------------\n".format(
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
                             "\nTransaction - "+each['trans_type']+
                             "\nAmount Charged - ${0:.2f}".format(each['amount_charged'])+"\n"
                             "Time Choice - "+each['time_choice']+
                             "\nDate Of - "+each['date_of_trans'].strftime('%m/%d/%Y %H:%M')+
                             "\nDue By - "+each['date_due']+"\n"
                             "Damaged on Return - "+str(each['return_info']['damaged'])+
                             "\nPast Due - "+str(each['return_info']['past_due'])+
                             "\n--------------------------\n")
                else:
                    trans = ("Item ID - "+each['item_id'].upper()+
                             "\nTransaction - "+each['trans_type']+
                             "\nAmount Charged - ${0:.2f}".format(each['amount_charged'])+"\n"
                             "Time Choice - "+each['time_choice']+
                             "\nDate Of - "+each['date_of_trans'].strftime('%m/%d/%Y %H:%M')+
                             "\nDue By - "+each['date_due'].strftime('%m/%d/%Y %H:%M')+"\n"
                             "Damaged on Return - "+str(each['return_info']['damaged'])+
                             "\nPast Due - "+str(each['return_info']['past_due'])+
                             "\n--------------------------\n")
                data_string += '\n'+trans
            return data_string
    else:
        return "\nI'm sorry, I didn't quite get that."


def view_total_revenue() -> str:
    """
    Displays total revenue to the user.
    """
    total = 0.0
    with open('trans_history.p', 'rb') as fin:
        history = pickle.load(fin)
        for each in history:
            total += float(each['amount_charged'])
    return 'Total Revenue: ${0:.2f}'.format(total)


if __name__ == '__main__':
    print(main())
