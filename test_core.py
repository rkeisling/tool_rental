"""These are the tests for core.py."""
from datetime import datetime
import core

# these just make the data layer fresh in order to avoid failed tests
core.initialize_inventory()
core.wipe_trans_history()
# these manipulate inventory and trans_history to test later functions
core.rent('generator', '3')
core.rent("air_compressor", '4')
core.rent('tilesaw', '1')


def test_rent():
    """
    Tests rent function in core.
    """
    assert core.rent('nailgun', '1') == "Item ID: {0}\nReturn By: {1}\nTotal Due: ${2:.2f}".format(
        'NAI5', core.calculate_return_date('5hour').strftime('%m/%d/%Y %H:%M'), 96.30
    )
    assert core.rent('jackhammer', '1') == ("I'm sorry, that item is currently unavailable. "
                                            "Please check again later.")
    assert core.rent('9', '2') == 'Have a nice day!'


def test_purchase():
    """
    Tests purchase function in core.
    """
    assert core.purchase("nailgun") == 'Total: ${0:.2f}\nItem ID: {1}'.format(
        321.00, 'nai4'
    )
    assert core.purchase('ballon') == ("I'm sorry, that item is currently unavailable. "
                                       "Please check again later.")
    assert core.purchase("9") == 'Have a nice day!'


def test_return_item():
    """
    Tests return_item in core.
    """
    assert core.return_item('nai5', False) == "Total: ${0:.2f}".format(-30.00)
    assert core.return_item('gen3', True) == "Total: ${0:.2f}".format(0.00)
    assert core.return_item('til1', False) == "Total: ${0:.2f}".format(-35.00)
    assert core.return_item('9', False) == 'Have a nice day!'


def test_replace_item():
    """
    Tests replace_item in core.
    """
    assert core.replace_item('air3') == 'Total: ${0:.2f}'.format(481.50)
    assert core.replace_item('water gun') == 'That is an invalid ID. Please try again.'


def test_is_late():
    """
    Tests is_late in core.
    """
    assert core.is_late('til1') == core.LateInfo(False, 0)
    assert core.is_late('air3') == ("I can't seem to find that item "
                                    "in the transaction history. Sorry!")


def test_choice_num_to_item():
    """
    Placeholder.
    """
    assert core.choice_num_to_item('1') == 'auger'
    assert core.choice_num_to_item('7') == 'That is not a valid choice.'


def test_get_price():
    """
    Placeholder.
    """
    assert core.get_price('nailgun') == 300
    assert core.get_price('generator') == 1500


def test_check_inventory():
    """
    Placeholder.
    """
    assert core.check_inventory('tilesaw') is True
    assert core.check_inventory('nailgun') is True


def test_item_id_to_item():
    """
    Placeholder.
    """
    assert core.item_id_to_item('nai3') == 'nailgun'
    assert core.item_id_to_item('air1') == 'air_compressor'
    assert core.item_id_to_item('water gun') == 'That is an invalid ID. Please try again.'


def test_update_inventory_remove():
    """
    Placeholder.
    """
    assert core.update_inventory_remove('generator') == 'gen3'


def test_is_valid_item():
    """
    Placeholder.
    """
    assert core.is_valid_item('nailgun') is True
    assert core.is_valid_item('water gun') is False


def test_get_time_diff():
    """
    Placeholder.
    """
    time_one = datetime(2017, 2, 2, 2, 51, 0)
    time_two = datetime(2017, 2, 9, 2, 51, 0)
    assert core.get_time_diff(time_two, time_one) == 168


def test_return_hours():
    """
    Placeholder.
    """
    time_three = datetime(2015, 3, 14, 9, 30, 0)
    time_four = datetime(2015, 3, 25, 3, 30, 0)
    assert core.return_hours(time_four - time_three) == 258
