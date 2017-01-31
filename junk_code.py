import datetime as DT


def rent(item, time_choice):
    """ (str, str) -> str, str
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
    with open('inventory.txt') as file:
        inv = file.readlines()
    price_rates = {'5hour': [.2, 'hours=5'],
                   '1day': [.3, 'days=1'],
                   '1week': [.6, 'days=7'],
                   '1month': [.9, 'days=30']}
    formatted_inv = [each.strip().split(' - ') for each in inv]
    for each in formatted_inv:
        if item == each[0]:
            price = float(each[1][1:])
    due = ((.1 * price) + (price_rates[time_choice][0] * price)) * 1.07
    today = DT.date.today()
    first_time = price_rates[time_choice][1]
    time_diff = first_time.rsplit('=', 1)[0]
    time_diff_val = first_time.rsplit("=", 1)[1]
    date_due = today - DT.timedelta(time_diff=time_diff_val)    
    form_str = """
    Tool ID: {0}
    Return By: {1}
    Total Due: ${2}
    """.format(item_id, date_due, due)
    return form_str

def purchase(item):
    """ (str, str) -> str
    Returns total price and ID of item purchased when given an item.
    Updates inventory using update_inventory().
    Updates transaction history using update_trans().
    """


def replace(item_id):
    """ (str) -> str
    Returns total price of replaced item.
    Updates inventory using update_inventory().
    Updates transaction history using update_trans().
    """

def update_inventory(item_id):
    """ (str) -> None
    Opens inventory.txt and updates it by adding or removing an item.
    """

def update_trans(item, item_id, total_price, return_date):
    """ (str, str, str, str) -> None
    Updates transaction history with the given information.
    """

def check_inventory(item):
    """ (str) -> bool
    Returns True or False depending if an item if available in inventory.txt.
    """

def return_item(item_id):
    """ (str) -> bool, str
    Returns if the item is late (determined using late_item()) and the total price.
    """

def late_item(item_id):
    """ (str) -> bool
    Returns if the given item is late or not by accessing transaction_history.txt.
    """

if __name__ == "__main__":
    item = input("What do you want?")
    how_long = input("How long?")
    rent(item, how_long)
