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

def getExpectedLines(idx): 
	'''
	Returns expected text based on a list of lines that should be printed
	'''
	
	logText = [
		"This is line 1/10\n",
		"This is line 2/10\n",
		"This is line 3/10\n",
		"This is line 4/10\n",
		"This is line 5/10 04:06:15\n",
		"This is line 6/10\n",
		"This is line 7/10\n",
		"This is line 8/10\n",
		"This is line 9/10\n",
		"This is line 10/10"
	]
	return "".join([logText[i] for i in idx if i < len(logText)  and i >= 0])

def getExpectedValuesForNoValueGiven(arg): 
	'''
	Returns values of the form (stdout, stderr) for when no value is given to -f or -l
	'''
	
	scriptName = PurePath(sys.argv[0]).parts[-1]
	return (
		"",
		f"usage: {scriptName} [-h] [-f NUM] [-l NUM] [-t] [-i] [-I] [FILE]\n{scriptName}: error: argument {arg}: expected one argument\n"
	)

def getExpectedValuesForInvalidValueGiven(arg, invalidVal): 
	'''
	Returns values of the form (stdout, stderr) for when an invalid value is given to -f or -l
	'''
	
	scriptName = PurePath(sys.argv[0]).parts[-1]
	return (
		"",
		f"usage: {scriptName} [-h] [-f NUM] [-l NUM] [-t] [-i] [-I] [FILE]\n{scriptName}: error: argument {arg}: invalid int value: '{invalidVal}'\n"
	)

'''
Positive tests
'''

@pytest.mark.parametrize("NUM", [0, 3, 10, 20])
def test_firstWithPositiveValues(capsys, NUM): 
	'''
	Tests -f NUM option with values >= 0
	Verifies that the entire log is printed if NUM > the log's length and no other options are used
	'''
	
	args = ["-f",str(NUM),"testLogs/test_firstAndLastOptions.log"]
	util.main(args)
	captured = capsys.readouterr()
	expected = getExpectedLines([i for i in range(0,NUM)])
	assert captured.out == expected
	assert captured.err == ""

@pytest.mark.parametrize("NUM", [-3, -10, -20])
def test_firstWithNegativeValues(capsys, NUM): 
	'''
	Tests -f NUM option with values < 0
	Verifies that a negative NUM value "counts from the back" (i.e., tells util to print the first n lines up to NUM from EOF)
	Verifies that no lines are printed if the absolute value of a negative NUM value exceeds the log's length
	'''
	
	args = ["--first",str(NUM),"testLogs/test_firstAndLastOptions.log"]
	util.main(args)
	captured = capsys.readouterr()
	expected = getExpectedLines([i for i in range(0,10+NUM)])
	assert captured.out == expected
	assert captured.err == ""

@pytest.mark.parametrize("NUM", [0, 3, 10, 20])
def test_lastWithPositiveValues(capsys, NUM): 
	'''
	Tests -l NUM option with values >= 0
	Verifies that the entire log is printed if NUM > the log's length and no other options are used
	'''
	
	args = ["-l",str(NUM),"testLogs/test_firstAndLastOptions.log"]
	util.main(args)
	captured = capsys.readouterr()
	expected = getExpectedLines([i for i in range(10-NUM,10)])
	assert captured.out == expected
	assert captured.err == ""

@pytest.mark.parametrize("NUM", [-3, -10, -20])
def test_lastWithNegativeValues(capsys, NUM): 
	'''
	Tests -l NUM option with values < 0
	Verifies that the entire log is printed if the absolute value of NUM > the log's length
	'''
	
	args = ["--last",str(NUM),"testLogs/test_firstAndLastOptions.log"]
	util.main(args)
	captured = capsys.readouterr()
	expected = getExpectedLines([i for i in range(10+NUM,10)])
	assert captured.out == expected
	assert captured.err == ""

@pytest.mark.parametrize("first,last", [("3","-3"),("7","3"),("-4","4")])
def test_firstAndLastNoOverlap(capsys, first, last): 
	'''
	Tests -f with -l when there is no intersection
	'''
	
	args = ["-f",first,"-l",last,"testLogs/test_firstAndLastOptions.log"]
	util.main(args)
	captured = capsys.readouterr()
	assert captured.out == ""
	assert captured.err == ""

@pytest.mark.parametrize("first,last,expectedIdx", 
	[
		("7","7",[3,4,5,6]),
		("8","-4",[6,7]),
		("-4","5",[5])
	]
)
def test_firstAndLastWithOverlap(capsys, first, last, expectedIdx): 
	'''
	Tests -f and -l when there is an intersection
	'''
	
	args = ["-f",first,"-l",last,"testLogs/test_firstAndLastOptions.log"]
	util.main(args)
	captured = capsys.readouterr()
	expected = getExpectedLines(expectedIdx)
	assert captured.out == expected
	assert captured.err == ""

def test_NoFirstOrLast(capsys): 
	'''
	Verifies that the absence of -f and -l does not prevent other options from producing output
	'''
	
	args = ["-t","testLogs/test_firstAndLastOptions.log"]
	util.main(args)
	captured = capsys.readouterr()
	expected = getExpectedLines([4])
	assert captured.out == expected
	assert captured.err == ""

@pytest.mark.parametrize("first,expected", 
	[
		(-15,[0,0]),
		(-10,[0,0]),
		(-5,[0,5]),
		(0,[0,0]),
		(5,[0,5]),
		(10,[0,10]),
		(15,[0,10])
	]
)
def test_calculateBoundsFirstOnly(first, expected): 
	'''
	Tests util.calculateBounds() with -f only
	'''
	
	assert util.calculateBounds(first,None,10) == expected

@pytest.mark.parametrize("last,expected", 
	[
		(-15,[0,10]),
		(-10,[0,10]),
		(-5,[5,10]),
		(0,[10,10]),
		(5,[5,10]),
		(10,[0,10]),
		(15,[0,10])
	]
)
def test_calculateBoundsLastOnly(last, expected): 
	'''
	Tests util.calculateBounds() with -l only
	'''
	
	assert util.calculateBounds(None,last,10) == expected

@pytest.mark.parametrize("first,last,expected", 
	[
		(-15,10,None),
		(10,-15,[0,10]),
		(10,10,[0,10]),
		(7,7,[3,7]),
		(8,-4,[6,8]),
		(-4,5,[5,6]),
		(3,-3,None),
		(7,3,None),
		(-4,4,None)
	]
)
def test_calculateBoundsBothFirstAndLast(first, last, expected): 
	'''
	Tests util.calculateBounds() with both -f and -l
	'''
	
	assert util.calculateBounds(first,last,10) == expected

def test_calculateBoundsNoFirstOrLast(): 
	'''
	Tests util.calculateBounds() with neither -f nor -l
	'''
	
	length = 10
	assert util.calculateBounds(None,None,length) == [0,length]

'''
Negative tests
'''

@pytest.mark.parametrize("shortArg,longArg", 
	[
		("-f","-f/--first"),
		("-l","-l/--last")
	]
)
def test_noValueGiven(capsys, shortArg, longArg): 
	'''
	Tests error handling when no value is given to -f or -l
	'''
	
	args = ["testLogs/test_firstAndLastOptions.log",shortArg]
	with pytest.raises(SystemExit): 
		util.main(args)
	captured = capsys.readouterr()
	expected_stdout, expected_stderr = getExpectedValuesForNoValueGiven(longArg)
	assert captured.out == expected_stdout
	assert captured.err == expected_stderr

@pytest.mark.parametrize("shortArg,longArg,invalidVal", 
	[
		("-f","-f/--first",".5"),
		("-f","-f/--first","str"),
		("-l","-l/--last",".5"),
		("-l","-l/--last","str")
	]
)
def test_invalidValueGiven(capsys, shortArg, longArg, invalidVal): 
	'''
	Tests error handling when an invalid value is given to -f or -l
	'''
	
	args = [shortArg,invalidVal,"testLogs/test_firstAndLastOptions.log"]
	with pytest.raises(SystemExit): 
		util.main(args)
	captured = capsys.readouterr()
	expected_stdout, expected_stderr = getExpectedValuesForInvalidValueGiven(longArg,invalidVal)
	assert captured.out == expected_stdout
	assert captured.err == expected_stderr
