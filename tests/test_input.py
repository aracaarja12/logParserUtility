import pytest
import sys
import os
import io
import re
import subprocess
from pathlib import PurePath

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import util

'''
Fixtures that return log paths
'''

@pytest.fixture
def logFromArg(): 
	return str(PurePath("testLogs/test_input_fromArg.log"))

@pytest.fixture
def logFromStdin(): 
	return str(PurePath("testLogs/test_input_fromStdin.log"))

@pytest.fixture
def invalidLog(): 
	return "invalid.log"

@pytest.fixture
def utilScript(): 
	return str(PurePath("../util.py"))

'''
Fixtures that return expected values of the form (stdout, stderr)
'''

@pytest.fixture
def expectedValuesReadingFromArg(): 
	return (
		"This is line 1 Reading from argument\n192.168.255.0 This is line 2 1762:0:0:0:0:B03:1:AF18\nThis is line 3 12:24:59\nThis is line 4 256.256.256.0\nThis is line 5 172.16.254.1", 
		""
	)

@pytest.fixture
def expectedValuesReadingFromStdin(): 
	return (
		"This is line 1 Reading from stdin\n192.168.255.0 This is line 2 1762:0:0:0:0:B03:1:AF18\nThis is line 3 12:24:59\nThis is line 4 256.256.256.0\nThis is line 5 172.16.254.1", 
		""
	)

@pytest.fixture
def expectedValuesForInvalidFile(invalidLog): 
	scriptName = PurePath(sys.argv[0]).parts[-1]
	return (
		"",
		f"usage: {scriptName} [-h] [-f NUM] [-l NUM] [-t] [-i] [-I] [FILE]\n{scriptName}: error: argument FILE: can't open '{invalidLog}': [Errno 2] No such file or directory: '{invalidLog}'\n"
	)

@pytest.fixture
def expectedValuesForNoInput(): 
	return (
		"", 
		"usage: util.py [-h] [-f NUM] [-l NUM] [-t] [-i] [-I] [FILE]\nutil.py: error: A file or standard input must be provided\n"
	)

'''
@pytest.fixture
def expectedValuesForNoInput(): 
	scriptName = PurePath(sys.argv[0]).parts[-1]
	return (
		"",
		f"usage: {scriptName} [-h] [-f NUM] [-l NUM] [-t] [-i] [-I] [FILE]\n{scriptName}: error: A file or standard input must be provided\n"
	)
'''

'''
Helper functions
'''

def runUtil(args): 
	'''
	Function runs util.py with the given arguments and returns (stdout, stderr, returncode)
	'''
	
	'''
	process = subprocess.run(args,capture_output=True,shell=True)
	
	# Decode and standardize stdout
	out = process.stdout.decode("utf-8")
	out = re.sub("\r","",out)
	
	# Decode and standardize stderr
	err = process.stderr.decode("utf-8")
	err = re.sub("\r","",err)
	
	return (out, err, process.returncode)
	'''
	out = None
	err = None
	
	if os.name == "nt": 
		process = subprocess.run(args,capture_output=True,shell=True)
		out = process.stdout
		err = process.stderr
	else: 
		process = subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		out, err = process.communicate()
	
	if out is not None: 
		out = out.decode("utf-8")
		out = re.sub("\r","",out)
	if err is not None: 
		err = err.decode("utf-8")
		err = re.sub("\r","",err)
	
	return (out, err)

'''
Positive tests
'''

def test_validArgNoStdin(capsys, logFromArg, expectedValuesReadingFromArg): 
	args = ["-f","5",logFromArg]
	util.main(args)
	captured = capsys.readouterr()
	expected_stdout, expected_stderr = expectedValuesReadingFromArg
	assert captured.out == expected_stdout
	assert captured.err == expected_stderr

def test_validArgWithStdin(capsys, monkeypatch, logFromArg, expectedValuesReadingFromStdin, expectedValuesReadingFromArg): 
	monkeypatch.setattr(sys, "stdin", io.StringIO(expectedValuesReadingFromStdin[0]))
	args = ["-f","5",logFromArg]
	util.main(args)
	captured = capsys.readouterr()
	expected_stdout, expected_stderr = expectedValuesReadingFromArg
	assert captured.out == expected_stdout
	assert captured.err == expected_stderr

def test_noArgWithStdin(capsys, monkeypatch, expectedValuesReadingFromStdin): 
	monkeypatch.setattr(sys, "stdin", io.StringIO(expectedValuesReadingFromStdin[0]))
	args = ["-f","5"]
	util.main(args)
	captured = capsys.readouterr()
	expected_stdout, expected_stderr = expectedValuesReadingFromStdin
	assert captured.out == expected_stdout
	assert captured.err == expected_stderr

'''
Negative tests
'''

def test_invalidArgNoStdin(capsys, invalidLog, expectedValuesForInvalidFile): 
	args = ["-f","5",invalidLog]
	with pytest.raises(SystemExit): 
		util.main(args)
	captured = capsys.readouterr()
	expected_stdout, expected_stderr = expectedValuesForInvalidFile
	assert captured.out == expected_stdout
	assert captured.err == expected_stderr

def test_invalidArgWithStdin(capsys, monkeypatch, invalidLog, expectedValuesReadingFromStdin, expectedValuesForInvalidFile): 
	monkeypatch.setattr(sys, "stdin", io.StringIO(expectedValuesReadingFromStdin[0]))
	args = ["-f","5",invalidLog]
	with pytest.raises(SystemExit): 
		util.main(args)
	captured = capsys.readouterr()
	expected_stdout, expected_stderr = expectedValuesForInvalidFile
	assert captured.out == expected_stdout
	assert captured.err == expected_stderr

def test_noArgNoStdin(utilScript, expectedValuesForNoInput): 
	actual_stdout, actual_stderr = runUtil([utilScript])
	expected_stdout, expected_stderr = expectedValuesForNoInput
	assert actual_stdout == expected_stdout
	assert actual_stderr == expected_stderr

'''
@pytest.mark.xfail
def test_noArgNoStdin(capsys, expectedValuesForNoInput): 
	args = ["-f","5"]
	util.parse_cli_args(args)
	captured = capsys.readouterr()
	expected_stdout, expected_stderr = expectedValuesForNoInput
	assert captured.out == expected_stdout
	assert captured.err == expected_stderr
'''


############ TODO cleanup below

'''
def test_commandLineArgumentAsInputFile(capsys, positionalArgumentArgs, expectedValue): 
	output = subprocess.check_output(positionalArgumentArgs,shell=True).decode("utf-8")
	output = re.sub("\r","",output)
	assert output == expectedValue

def test_stdinAsInputFile(capsys, stdinArgs, expectedValue): 
	output = subprocess.check_output(stdinArgs,shell=True).decode("utf-8")
	output = re.sub("\r","",output)
	assert output == expectedValue
'''
	
'''
log = "test_input.log"
args = ["-f","5",f"testLogs/{log}"]
util.main(args)
captured = capsys.readouterr()
assert captured.out == expectedValue
'''

'''
#args = ["..\\util.py", "testLogs\\invalid.log"]
#args = ["..\\util.py", "-f", "5", "testLogs\\test_input_fromArg.log"]
#args = ["type", "testLogs\\test_input_fromStdin.log", "|", "..\\util.py", "testLogs\\invalid.log"]
args = ["..\\util.py"]
output = subprocess.run(args,capture_output=True,shell=True)
so = output.stdout.decode("utf-8")
se = output.stderr.decode("utf-8")
sn = output.returncode

print(repr(so))
print(repr(se))
print(repr(sn))
'''
