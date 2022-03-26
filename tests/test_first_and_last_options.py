import pytest
import sys
import os
from pathlib import PurePath

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import util

'''
Helper functions
'''

def get_expected_lines(idx): 
    '''
    Returns expected text based on a list of lines that should be printed
    '''
    
    log_text = (
        "This is line 1/10\n",
        "This is line 2/10\n",
        "This is line 3/10\n",
        "This is line 4/10\n",
        "This is line 5/10\n",
        "This is line 6/10\n",
        "This is line 7/10\n",
        "This is line 8/10\n",
        "This is line 9/10\n",
        "This is line 10/10"
    )
    return "".join([log_text[i] for i in idx if i < len(log_text)  and i >= 0])

def get_expected_values_for_no_value_given(arg): 
    '''
    Returns values of the form (stdout, stderr) for when no value is given to -f or -l
    '''
    
    script_name = PurePath(sys.argv[0]).parts[-1]
    return (
        "",
        f"usage: {script_name} [-h] [-f NUM] [-l NUM] [-t] [-i] [-I] [FILE]\n{script_name}: error: argument {arg}: expected one argument\n"
    )

def get_expected_values_for_invalid_value_given(arg, invalid_val): 
    '''
    Returns values of the form (stdout, stderr) for when an invalid value is given to -f or -l
    '''
    
    script_name = PurePath(sys.argv[0]).parts[-1]
    return (
        "",
        f"usage: {script_name} [-h] [-f NUM] [-l NUM] [-t] [-i] [-I] [FILE]\n{script_name}: error: argument {arg}: invalid int value: '{invalid_val}'\n"
    )

'''
Positive tests
'''

@pytest.mark.parametrize("NUM", [0, 3, 10, 20])
def test_first_with_positive_values(capsys, NUM): 
    '''
    Tests -f NUM option with values >= 0
    Verifies that the entire log is printed if NUM > the log's length and no other options are used
    '''
    
    args = ["-f", str(NUM), "testLogs/test_first_and_last_options.log"]
    util.main(args)
    captured = capsys.readouterr()
    expected = get_expected_lines([i for i in range(0,NUM)])
    assert captured.out == expected
    assert captured.err == ""

@pytest.mark.parametrize("NUM", [-3, -10, -20])
def test_first_with_negative_values(capsys, NUM): 
    '''
    Tests -f NUM option with values < 0
    Verifies that a negative NUM value "counts from the back" (i.e., tells util to print the first n lines up to NUM from EOF)
    Verifies that no lines are printed if the absolute value of a negative NUM value exceeds the log's length
    '''
    
    args = ["--first", str(NUM), "testLogs/test_first_and_last_options.log"]
    util.main(args)
    captured = capsys.readouterr()
    expected = get_expected_lines([i for i in range(0,10+NUM)])
    assert captured.out == expected
    assert captured.err == ""

@pytest.mark.parametrize("NUM", [0, 3, 10, 20])
def test_last_with_positive_values(capsys, NUM): 
    '''
    Tests -l NUM option with values >= 0
    Verifies that the entire log is printed if NUM > the log's length and no other options are used
    '''
    
    args = ["-l", str(NUM), "testLogs/test_first_and_last_options.log"]
    util.main(args)
    captured = capsys.readouterr()
    expected = get_expected_lines([i for i in range(10-NUM,10)])
    assert captured.out == expected
    assert captured.err == ""

@pytest.mark.parametrize("NUM", [-3, -10, -20])
def test_last_with_negative_values(capsys, NUM): 
    '''
    Tests -l NUM option with values < 0
    Verifies that the entire log is printed if the absolute value of NUM > the log's length
    '''
    
    args = ["--last", str(NUM), "testLogs/test_first_and_last_options.log"]
    util.main(args)
    captured = capsys.readouterr()
    expected = get_expected_lines([i for i in range(10+NUM,10)])
    assert captured.out == expected
    assert captured.err == ""

@pytest.mark.parametrize("first,last", [("3", "-3"),("7", "3"),("-4", "4")])
def test_first_and_last_no_overlap(capsys, first, last): 
    '''
    Tests -f with -l when there is no intersection
    '''
    
    args = ["-f", first, "-l", last, "testLogs/test_first_and_last_options.log"]
    util.main(args)
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""

@pytest.mark.parametrize("first,last,expected_idx", 
    [
        ("7", "7", [3, 4, 5, 6]),
        ("8", "-4", [6, 7]),
        ("-4", "5", [5])
    ]
)
def test_first_and_last_with_overlap(capsys, first, last, expected_idx): 
    '''
    Tests -f and -l when there is an intersection
    '''
    
    args = ["-f", first, "-l", last, "testLogs/test_first_and_last_options.log"]
    util.main(args)
    captured = capsys.readouterr()
    expected = get_expected_lines(expected_idx)
    assert captured.out == expected
    assert captured.err == ""

@pytest.mark.parametrize("first,expected", 
    [
        (-15, [0, 0]),
        (-10, [0, 0]),
        (-5, [0, 5]),
        (0, [0, 0]),
        (5, [0, 5]),
        (10, [0, 10]),
        (15, [0, 10])
    ]
)
def test_calculate_bounds_first_only(first, expected): 
    '''
    Tests util.calculate_bounds() with -f only
    '''
    
    assert util.calculate_bounds(first, None, 10) == expected

@pytest.mark.parametrize("last,expected", 
    [
        (-15, [0, 10]),
        (-10, [0, 10]),
        (-5, [5, 10]),
        (0, [10, 10]),
        (5, [5, 10]),
        (10, [0, 10]),
        (15, [0, 10])
    ]
)
def test_calculate_bounds_last_only(last, expected): 
    '''
    Tests util.calculate_bounds() with -l only
    '''
    
    assert util.calculate_bounds(None, last, 10) == expected

@pytest.mark.parametrize("first,last,expected", 
    [
        (-15, 10, None),
        (10, -15, [0, 10]),
        (10, 10, [0, 10]),
        (7, 7, [3, 7]),
        (8, -4, [6, 8]),
        (-4, 5, [5, 6]),
        (3, -3, None),
        (7, 3, None),
        (-4, 4, None)
    ]
)
def test_calculate_bounds_both_first_and_last(first, last, expected): 
    '''
    Tests util.calculate_bounds() with both -f and -l
    '''
    
    assert util.calculate_bounds(first, last, 10) == expected

def test_calculate_bounds_no_first_or_last(): 
    '''
    Tests util.calculate_bounds() with neither -f nor -l
    '''
    
    length = 10
    assert util.calculate_bounds(None, None, length) == [0, length]

'''
Negative tests
'''

@pytest.mark.parametrize("short_arg,long_arg", 
    [
        ("-f", "-f/--first"),
        ("-l", "-l/--last")
    ]
)
def test_no_value_given(capsys, short_arg, long_arg): 
    '''
    Tests error handling when no value is given to -f or -l
    '''
    
    args = ["testLogs/test_first_and_last_options.log", short_arg]
    with pytest.raises(SystemExit): 
        util.main(args)
    captured = capsys.readouterr()
    expected_stdout, expected_stderr = get_expected_values_for_no_value_given(long_arg)
    assert captured.out == expected_stdout
    assert captured.err == expected_stderr

@pytest.mark.parametrize("short_arg,long_arg,invalid_val", 
    [
        ("-f", "-f/--first", ".5"),
        ("-f", "-f/--first", "str"),
        ("-l", "-l/--last", ".5"),
        ("-l", "-l/--last", "str")
    ]
)
def test_invalid_value_given(capsys, short_arg, long_arg, invalid_val): 
    '''
    Tests error handling when an invalid value is given to -f or -l
    '''
    
    args = [short_arg, invalid_val, "testLogs/test_first_and_last_options.log"]
    with pytest.raises(SystemExit): 
        util.main(args)
    captured = capsys.readouterr()
    expected_stdout, expected_stderr = get_expected_values_for_invalid_value_given(long_arg,invalid_val)
    assert captured.out == expected_stdout
    assert captured.err == expected_stderr
