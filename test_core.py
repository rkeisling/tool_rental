"""These are the tests for core.py."""
from datetime import datetime
import core

# these just make the data layer fresh in order to avoid failed tests
core.initialize_inventory()
core.wipe_trans_history()
# these manipulate inventory and trans_history to test later functions
core.rent('generator', '3')
core.rent("air_compressor", '4')
core.rent('pressure_washer', '2')
core.purchase("pressure_washer")


# rent tests
def test_rent_normal():
    """
    Tests normal functionality of the rent function.
    """
    assert core.rent(
        'nailgun', '1') == "\nItem ID: {0}\nReturn By: {1}\nTotal Due: ${2:.2f}".format(
            'NAI5', core.calculate_return_date('5hour').strftime('%m/%d/%Y %H:%M'), 96.30
        )


def test_rent_not_an_item():
    """
    Tests the rent fucntion on an item that isn't in the inventory.
    """
    assert core.rent('jackhammer', '1') == ("\nI'm sorry, that item is currently unavailable. "
                                            "Please check again later.")


def test_rent_cancel():
    """
    Tests canceling out of the program through the rent function.
    """
    assert core.rent('9', '2') == '\nHave a nice day!'


# purchase tests
def test_purchase_normal():
    """
    Tests normal functionality of purchase function.
    """
    assert core.purchase("nailgun") == '\nTotal: ${0:.2f}\nItem ID: {1}'.format(
        321.00, 'NAI4'
    )


def test_purchase_not_item():
    """
    Tests purchase on an item that isn't (and was never) in the inventory.
    """
    assert core.purchase('balloon') == ("\nI'm sorry, that item is currently unavailable. "
                                        "Please check again later.")


def test_purchase_cancel():
    """
    Tests cancelling out of the program through the purchase function.
    """
    assert core.purchase("9") == '\nHave a nice day!'


# replace_item tests
def test_replace_item_normal():
    """
    Tests normal functionality of replace_item function.
    """
    assert core.replace_item('air3') == '\nTotal: ${0:.2f}'.format(481.50)


def test_replace_item_not_item():
    """
    Tests replace_item on an item that isn't in the inventory.
    """
    assert core.replace_item('water gun') == '\nThat is an invalid ID. Please try again.'


def test_replace_item_cancel():
    """
    Tests cancelling out of the program through replace_item.
    """
    assert core.replace_item('9') == '\nHave a nice day!'


# return_item tests
def test_return_item_normal():
    """
    Tests normal functionality of return_item.
    """
    assert core.return_item('nai5', False) == "\nTotal: ${0:.2f}".format(-30.00)


def test_return_item_damaged():
    """
    Tests returning a damaged item.
    """
    assert core.return_item('gen3', True) == "\nTotal: ${0:.2f}".format(0.00)


def test_return_item_not_rented():
    """
    Tests the return_item function on an item that wasn't rented (still in inventory).
    """
    assert core.return_item(
        'til1', False) == "\nI can't seem to find that item in the transaction history. Sorry!"


def test_return_item_cancel():
    """
    Tests cancelling out of the program through the return_item function.
    """
    assert core.return_item('9', False) == '\nHave a nice day!'


def test_return_item_invalid():
    """
    Tests passing an invalid ID into return_item.
    """
    assert core.return_item('potato', False) == "\nThat is an invalid ID. Please try again."


def test_return_item_replaced():
    """
    Tests passing in an item that is in the transaction history as rented,
    but was later replaced.
    """
    assert core.return_item(
        "air3", False) == "\nI can't seem to find that item in the transaction history. Sorry!"


# is_late tests
def test_is_late_normal():
    """
    Tests normal functionality of is_late.
    """
    assert core.is_late('pre2') == core.LateInfo(False, 0)


def test_is_late_not_in_inv():
    """
    Tests is_late on an item that isn't in the transaction history.
    """
    assert core.is_late('til1') == ("\nI can't seem to find that item "
                                    "in the transaction history. Sorry!")


# choice_num_to_item tests
def test_choice_num_to_item_normal():
    """
    Tests normal functionality of choice_num_to_item.
    """
    assert core.choice_num_to_item('1') == 'auger'


def test_choice_num_to_item_invalid():
    """
    Tests passing an invalid choice into choice_num_to_item.
    """
    assert core.choice_num_to_item('7') == '\nThat is not a valid choice.'


# get_price test
def test_get_price_normal():
    """
    Tests normal functionality of get_price.
    """
    assert core.get_price('nailgun') == 300
    assert core.get_price('generator') == 1500


# check_inventory tests
def test_check_inventory_normal():
    """
    Tests normal functionality of check_inventory.
    """
    assert core.check_inventory('tilesaw') is True
    assert core.check_inventory('nailgun') is True


def test_check_inventory_empty():
    """
    Tests check inventory for when the item is unavailable.
    """
    assert core.check_inventory('pressure_washer') is False


# item_id_to_item tests
def test_item_id_to_item_normal():
    """
    Tests normal functionality of item_id_to_item.
    """
    assert core.item_id_to_item('nai3') == 'nailgun'
    assert core.item_id_to_item('air1') == 'air_compressor'


def test_item_id_to_item_invalid():
    """
    Tests passing an invalid ID into item_id_to_item.
    """
    assert core.item_id_to_item('water gun') == '\nThat is an invalid ID. Please try again.'


# update_inv_rem test
def test_update_inv_rem_normal():
    """
    Tests normal functionality of update_inv_rem.
    """
    assert core.update_inv_rem('generator') == 'gen3'


# is_valid_item test
def test_is_valid_item_normal():
    """
    Tests normal functionality of is_valid_item.
    """
    assert core.is_valid_item('nailgun') is True
    assert core.is_valid_item('water gun') is False


# get_time_diff test
def test_get_time_diff_normal():
    """
    Tests normal functionality of get_time_diff.
    """
    time_one = datetime(2017, 2, 2, 2, 51, 0)
    time_two = datetime(2017, 2, 9, 2, 51, 0)
    assert core.get_time_diff(time_two, time_one) == 168


# return_hours test
def test_return_hours_normal():
    """
    Tests normal functionality of return_hours.
    """
    time_three = datetime(2015, 3, 14, 9, 30, 0)
    time_four = datetime(2015, 3, 25, 3, 30, 0)
    assert core.return_hours(time_four - time_three) == 258
