from decimal import Decimal

from ..eval import safe_eval


def test_bool_op_and():
    assert not safe_eval("True and False")
    assert safe_eval("True and True")
    assert safe_eval("True and True and True")
    assert not safe_eval("False and False")
    assert safe_eval("True and True and True")
    assert not safe_eval("True and True and False")


def test_bool_op_or():
    assert safe_eval("True or False")
    assert safe_eval("True or True")
    assert not safe_eval("False or False")
    assert not safe_eval("False or False or False")
    assert safe_eval("True or True or False")


def test_bool_op_and_or():
    assert safe_eval("True and True or False")
    assert not safe_eval("True and False or False")


def test_unary_not():
    assert safe_eval("True and not False")
    assert not safe_eval("False and not True and not False")


def test_bin_multiply():
    assert safe_eval("12 * 3 * 2") == 72
    assert safe_eval("round(0.2 * 3 * 0.2, 2)") == 0.12


def test_bin_add():
    assert safe_eval("12 + 3 + 2") == 17
    assert safe_eval("round(0.2 + 3 + 0.2, 1)") == 3.4


def test_bin_subtract():
    assert safe_eval("12 - 3 - 2") == 7
    assert safe_eval("0.2 - 3 - 0.2") == -3


def test_bin_divide():
    assert safe_eval("12 / 3 / 2") == 2
    assert safe_eval("round(0.2 / 3 / 0.2, 3)") == 0.333


def test_bin_pow():
    assert safe_eval("12 ** 3") == 144 * 12


def test_comparator_equals():
    assert safe_eval("2 == 1 + 1")
    assert not safe_eval("3 == 1 + 1")


def test_comparator_not_equals():
    assert safe_eval("3 != 1 + 1")
    assert not safe_eval("3 != 1 + 2")


def test_comparator_greater_than():
    assert safe_eval("3 > 2")
    assert not safe_eval("2 > 2")


def test_comparator_greater_than_or_equals():
    assert safe_eval("2 >= 2")
    assert not safe_eval("1 >= 2")


def test_comparator_less_than():
    assert safe_eval("2 < 3")
    assert not safe_eval("2 < 2")


def test_comparator_less_than_or_equals():
    assert safe_eval("2 <= 2")
    assert not safe_eval("2 <= 1")


def test_comparator_is():
    assert safe_eval("None is None")
    assert safe_eval("True is True")
    assert not safe_eval("True is None")


def test_comparator_is_not():
    assert safe_eval("True is not None")
    assert not safe_eval("True is not True")


def test_comparator_in():
    assert safe_eval("1 in [1, 2]")
    assert safe_eval("'banana' in ['apple', 'banana']")
    assert not safe_eval("'custard' in ['crumble', 'potato']")


def test_comparator_not_in():
    assert not safe_eval("1 not in [1, 2]")
    assert not safe_eval("'banana' not in ['apple', 'banana']")
    assert safe_eval("'custard' not in ['crumble', 'potato']")


def test_sum():
    assert safe_eval("sum([1, 2, 3])") == 6


def test_float():
    assert safe_eval("float(1)") == 1.0


def test_int():
    assert safe_eval("int(1.0)") == 1


def test_str():
    assert safe_eval("str(1)") == "1"


def test_round():
    assert safe_eval("round(1.234, 1)") == 1.2


def test_any():
    assert safe_eval("any([True, False])")
    assert not safe_eval("any([False, False])")


def test_all():
    assert safe_eval("all([True, True])")
    assert not safe_eval("all([True, False])")


def test_decimal():
    assert safe_eval("Decimal(1.23)") == Decimal(1.23)


def test_bitwise_and():
    assert safe_eval("8 & 15") == 8


def test_bitwise_or():
    assert safe_eval("8 | 15") == 15


def test_bitwise_xor():
    assert safe_eval("8 ^ 15") == 7
