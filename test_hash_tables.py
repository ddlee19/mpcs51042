'''
Final Project: Speaker Recognition System
Lamont Samuels
May 2020
'''

from itertools import permutations
import os
import pytest

from hash_table import Hashtable

# Get the name of the directory that holds the grading code.
BASE_DIR = os.path.dirname(__file__)

KEY1 = "key"
DEF_VAL1 = (None,(None,None))

################## Simple Hash Table Tests##################
def helper_update(table, test_dict):
    '''
    Purpose: Adds a test dictionary key, values to a HashTable object
    '''
    for key, value in test_dict.items():
        table[key] = value


def checkTest(test_keys,actual_results,expected_results):
    # 2nd: Check to the actual results to see if they match the expected values
    failed = False
    expected_values = list(expected_results.values())
    for idx, actual_result in enumerate(actual_results):
        expected_result = expected_values[idx]
        if expected_result is None:
            if actual_result is not None:
                failed = True
                break
        elif actual_result != expected_result:
            failed = True
            break

    if failed:
        actual_results = dict(zip(test_keys, actual_results))
        s = ("Expected (key, value) pairs ({:}) \n\n\n and actual "
             "(key, value) pairs ({:}) do not match in hash table.")
        pytest.fail(s.format(expected_results, actual_results))

def helper_lst(message, keys_values, actual,expected):

    if len(expected) != len(actual):
        s = f'Items in hashtable = {keys_values}\ntable.{message}() actual = {actual}\ntable.keys() expected = {expected}' 
        pytest.fail(s)
        
    actual = list(iter(actual))
    all_equal = True  
    for val in expected: 
        if val not in actual:
            all_equal = False 
            break 

    if not all_equal:
        s = f'Items in hashtable = {keys_values}\ntable.{message}() actual = {actual}\ntable.keys() expected = {expected}' 
        pytest.fail(s)

def helper_contains(table, expected_results):
    test_keys = list(expected_results.keys())

    # 1st: Call contains on the test_keys
    actual_results = []
    for key in test_keys:
        actual_results.append(key in table)

    # 2nd: Check to the actual results to see if they match the expected values
    checkTest(test_keys,actual_results,expected_results)


def helper_lookup(table, expected_results):
    '''
    Purpose: helper function for testing lookup

    Inputs:
        table: (HashTable) the hash table used to perform the lookup
        key: (string) a string to lookup in the hash table
    '''
    test_keys = list(expected_results.keys())

    # 1st: Call lookup on the test_keys
    actual_results = []
    for key in test_keys:
        actual_results.append(table[key])


    # 2nd: Check to the actual results to see if they match the expected values
    checkTest(test_keys,actual_results,expected_results)

def simple_1(table):
    '''
    Purpose: Test a lookup on an empty table
    '''
    helper_lookup(table, {KEY1:None})

def simple_2(table):
    '''
    Purpose: Check the def-value which can be anything is return on 
    an empty table 
    '''
    helper_lookup(table, {KEY1:DEF_VAL1})

def simple_3(table):
    '''
    Purpose: Test a update/lookup on a single item
    '''
    table["key"] = 1
    helper_lookup(table, {KEY1:1})

def simple_4(table):
    '''
    Purpose: Test a update/lookup on a single item
    '''
    table["key"] = 1
    helper_lookup(table, {KEY1:1})

def simple_5(table):
    '''
    Purpose: Test a update/lookup on a small set of items
    '''
    keys = [''.join(tup) for tup in list(permutations("abc"))]
    test_dict = dict(zip(keys, range(len(keys))))
    helper_update(table, test_dict)
    helper_lookup(table, test_dict)


def simple_6(table):
    '''
    Purpose: Test a update/lookup on a small set of items
    '''
    keys = [''.join(tup) for tup in list(permutations("abc"))]
    test_dict = dict(zip(keys, range(len(keys))))
    helper_update(table, test_dict)
    helper_lookup(table, test_dict)

def simple_7(table):
    '''
    Purpose: Test a update/lookup on a small set of items with some of the
    keys not being inside of the hash table
    '''
    keys = [''.join(tup) for tup in list(permutations("abc"))]
    test_dict = dict(zip(keys, range(len(keys))))
    helper_update(table, test_dict)

    # Add to the test dictionary of a set of keys that will NOT be in
    # the dictionary they should all return the default value, which
    # in this case is "None"
    not_table_keys = [''.join(tup) for tup in list(permutations("test"))]
    not_table_values = [None] * len(not_table_keys)
    test_dict.update(dict(zip(not_table_keys, not_table_values)))
    helper_lookup(table, test_dict)

def simple_8(table):
    '''
    Purpose: Test a update/lookup on a larger set items,
    '''
    keys = [''.join(tup) for tup in list(permutations("abcefgh"))]
    test_dict = dict(zip(keys, range(len(keys))))
    helper_update(table, test_dict)
    helper_lookup(table, test_dict)

def simple_9(table):
    '''
    Purpose: Test a update/lookup on a larger set of items
        1st: Adding an initial set of key/value pairs
        2nd: Updating the values for the original key value pairs
    '''
    keys = [''.join(tup) for tup in list(permutations("abcefgh"))]
    test_dict1 = dict(zip(keys, range(len(keys))))
    test_dict2 = dict(zip(keys, [i + 100 for i in range(len(keys))]))
    helper_update(table, test_dict1)
    helper_update(table, test_dict2)
    helper_lookup(table, test_dict2)

def simple_10(table):
    '''
    Purpose simple contains test on an empty table 
    ''' 
    helper_contains(table, {KEY1:False})

def simple_11(table):
    '''
    Purpose: Test a update/lookup on a larger set of items
        1st: Adding an initial set of key/value pairs
        2nd: Check contains to see if it does or does not contain a set of items. 
    '''
    keys = [''.join(tup) for tup in list(permutations("abc"))]
    test_dict = dict(zip(keys, [True] * len(keys)))
    helper_update(table, test_dict)

    # Add to the test dictionary of a set of keys that will NOT be in
    # the dictionary they should all return the default value, which
    # in this case is "None"
    not_table_keys = [''.join(tup) for tup in list(permutations("test"))]
    not_table_values = [False] * len(not_table_keys)
    test_dict.update(dict(zip(not_table_keys, not_table_values)))
    helper_contains(table, test_dict)

def simple_12(table):
    '''
    Purpose simple keys() test on an empty table 
    ''' 
    # 2nd: Check to the actual results to see if they match the expected values
    helper_lst("keys", [], table.keys(), [])

def simple_13(table):
    '''
    Purpose simple keys() test on a table 
    ''' 
    keys = [''.join(tup) for tup in list(permutations("abcd"))]
    test_dict = dict(zip(keys, range(len(keys))))
    helper_update(table, test_dict)
    # 2nd: Check to the actual results to see if they match the expected values
    helper_lst("keys", test_dict, table.keys(),keys)

def simple_14(table):
    '''
    Purpose simple values() test on an empty table 
    ''' 
    # 2nd: Check to the actual results to see if they match the expected values
    helper_lst("values", [], table.values(), [])

def simple_15(table):
    '''
    Purpose simple values() test on a table 
    ''' 
    keys = [''.join(tup) for tup in list(permutations("abcd"))]
    test_dict = dict(zip(keys, range(len(keys))))
    helper_update(table, test_dict)
    # 2nd: Check to the actual results to see if they match the expected values
    helper_lst("values", test_dict, table.values(),range(len(keys)))

def simple_16(table):
    '''
    Purpose simple iter() test on an empty table 
    ''' 
    # 2nd: Check to the actual results to see if they match the expected values
    helper_lst("values", [], list(iter(table)), [])

def simple_17(table):
    '''
    Purpose simple iter() test on a table 
    ''' 
    keys = [''.join(tup) for tup in list(permutations("abcd"))]
    test_dict = dict(zip(keys, range(len(keys))))
    helper_update(table, test_dict)
    # 2nd: Check to the actual results to see if they match the expected values
    helper_lst("values", test_dict, list(iter(table)), list(zip(keys, range(len(keys)))))


def simple_18(table):
    '''
    Purpose simple iter() test on a table 
    ''' 
    actual = len(table)
    expected = 0 
    if len(table) != expected:
        s = f'Items in hashtable = {[]}\nlen(table) actual = {actual}\nlen(table) expected = {expected}' 
        pytest.fail(s)

def simple_19(table):
    '''
    Purpose simple iter() test on a table 
    ''' 
    keys = [''.join(tup) for tup in list(permutations("abcd"))]
    test_dict = dict(zip(keys, range(len(keys))))
    helper_update(table, test_dict)

    actual = len(table)
    expected = len(keys) 
    if len(table) != expected:
        s = f'Items in hashtable = {[]}\nlen(table) actual = {actual}\nlen(table) expected = {expected}' 
        pytest.fail(s)

def simple_20(table):
    '''
    Purpose simple iter() test on a table 
    ''' 
    actual = bool(table)
    expected = False 
    if len(table) != expected:
        s = f'Items in hashtable = {[]}\nbool(table) actual = {actual}\nbool(table) expected = {expected}' 
        pytest.fail(s)


def simple_21(table):
    '''
    Purpose simple iter() test on a table 
    ''' 
    keys = [''.join(tup) for tup in list(permutations("abcd"))]
    test_dict = dict(zip(keys, range(len(keys))))
    helper_update(table, test_dict)

    actual = bool(table)
    expected = True 
    if actual == False:
        s = f'Items in hashtable = {[]}\nbool(table) actual = {actual}\nbool(table) expected = {expected}' 
        pytest.fail(s)

def simple_22(table):
    '''
    Purpose simple delete test for deleting small amount of items 
    ''' 
    keys = [''.join(tup) for tup in list(permutations("abc"))]
    test_dict = dict(zip(keys, range(len(keys))))
    helper_update(table, test_dict)

    #Now lets delete a few items 
    del table["cab"]
    del table["abc"]
    del table["cba"]

    del test_dict["cab"]
    del test_dict["abc"]
    del test_dict["cba"]

    actual = len(table)
    expected = len(test_dict) 
    if len(table) != expected:
        s = f'Items in hashtable = {[]}\nDeleted:"cab","abc","cba",\nlen(table) actual = {actual}\nlen(table) expected = {expected}' 
        pytest.fail(s)

    helper_lookup(table,test_dict)

def simple_23(table):
    '''
    Purpose simple delete test for deleting all items in the table. 
    ''' 
    keys = [''.join(tup) for tup in list(permutations("abcefgh"))]
    test_dict = dict(zip(keys, range(len(keys))))
    helper_update(table, test_dict)

    #Now lets delete all items 
    for key in keys:
        del table[key]

    actual = len(table)
    expected = 0
    if len(table) != expected:
        s = f'Items in hashtable = {test_dict}\nDeleted:all items,\nlen(table) actual = {actual}\nlen(table) expected = {expected}' 
        pytest.fail(s)


def test_init_1():
    table = Hashtable(1, None, 0.5, 2)
    simple_1(table) 

def test_init_2():
    table = Hashtable(1, DEF_VAL1, 0.5, 2)
    simple_2(table) 

def test_getset_3():
    table = Hashtable(1, None, 0.5, 2)
    simple_3(table) 

def test_getset_4():
    table = Hashtable(1, None, 0.5, 2)
    simple_4(table) 

def test_getset_5():
    table = Hashtable(50, None, 0.5, 2)
    simple_5(table) 

def test_getset_6():
    table = Hashtable(50, None, 0.5, 2)
    simple_6(table)

def test_getset_7():
    table = Hashtable(50, None, 0.5, 2)
    simple_7(table) 

def test_getset_8():
    table = Hashtable(12000, None, 0.5, 2)
    simple_8(table) 

def test_getset_9():
    table = Hashtable(12000, None, 0.5, 2)
    simple_9(table) 

def test_contains_10():
    table = Hashtable(1, None, 0.5, 2)
    simple_10(table) 

def test_contains_11():
    table = Hashtable(50, None, 0.5, 2)
    simple_10(table) 

def test_keys_12():
    table = Hashtable(1, None, 0.5, 2)
    simple_12(table) 

def test_keys_13():
    table = Hashtable(12000, None, 0.5, 2)
    simple_13(table) 

def test_values_14():
    table = Hashtable(1, None, 0.5, 2)
    simple_14(table) 

def test_values_15():
    table = Hashtable(12000, None, 0.5, 2)
    simple_15(table) 

def test_iter_16():
    table = Hashtable(1, None, 0.5, 2)
    simple_16(table)

def test_iter_17():
    table = Hashtable(12000, None, 0.5, 2)
    simple_17(table) 

def test_len_18():
    table = Hashtable(1, None, 0.5, 2)
    simple_18(table)

def test_len_19():
    table = Hashtable(12000, None, 0.5, 2)
    simple_19(table) 

def test_bool_20():
    table = Hashtable(1, None, 0.5, 2)
    simple_20(table) 

def test_bool_21():
    table = Hashtable(12000, None, 0.5, 2)
    simple_21(table) 

def test_del_22():
    table = Hashtable(1, None, 0.5, 2)
    simple_22(table) 

def test_del_23():
    table = Hashtable(12000, None, 0.5, 2)
    simple_23(table) 

################## Rehash Hash Table Tests ##################
def test_rehash_1():
    '''
    Purpose: Testing rehashing on a small set of items
    '''
    table = Hashtable(1, None, 0.5, 2)
    keys = [''.join(tup) for tup in list(permutations("abcd"))]
    test_dict1 = dict(zip(keys, range(len(keys))))
    helper_update(table, test_dict1)
    helper_lookup(table, test_dict1)

def test_rehash_2():
    '''
    Purpose: Testing rehashing on a larger set of items
    '''
    table = Hashtable(1, None, 0.5, 2)
    keys = [''.join(tup) for tup in list(permutations("abcefgh"))]
    test_dict1 = dict(zip(keys, range(len(keys))))
    helper_update(table, test_dict1)
    helper_lookup(table, test_dict1)

def test_rehash_3():
    '''
    Purpose: Test rehashing on a small set that wraps around
    '''
    keys = [chr(i) for i in range(ord('f'), ord('z'))]
    test_dict1 = dict(zip(keys, range(len(keys))))
    table = Hashtable(15, None, 0.5, 2)
    helper_update(table, test_dict1)
    helper_lookup(table, test_dict1)
