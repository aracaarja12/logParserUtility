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

'''
@pytest.fixture
def expectedValuesForInvalidFile(): 
	return (
		"",
		"usage: util.py [-h] [-f NUM] [-l NUM] [-t] [-i] [-I] [FILE]\nutil.py: error: argument FILE: can't open 'invalid.log': [Errno 2] No such file or directory: 'invalid.log'\n"
	)
'''

@pytest.fixture
def expectedValuesForInvalidFile(invalidLog): 
	scriptName = PurePath(sys.argv[0]).parts[-1]
	return (
		"",
		f"usage: {scriptName} [-h] [-f NUM] [-l NUM] [-t] [-i] [-I] [FILE]\n{scriptName}: error: argument FILE: can't open '{invalidLog}': [Errno 2] No such file or directory: '{invalidLog}'\n"
	)

'''
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
def getArgs(key): 
	#Function fetches arguments for util.py from a dictionary
	
	util = PurePath("../util.py")
	logFromArg = PurePath("testLogs/test_input_fromArg.log")
	logFromStdin = PurePath("testLogs/test_input_fromStdin.log")
	printCmd = "type" if os.name == "nt" else "cat"
	
	args = {
		"validArgNoPipe" : ["-f", "5", logFromArg], 
		"validArgWithPipe" : [printCmd, logFromStdin, "|", util, "-f", "5", logFromArg],  
		"invalidArgNoPipe" : [util, "invalid.log"], 
		"invalidArgWithPipe" : [printCmd, logFromStdin, "|", util, "invalid.log"], 
		"noArgNoPipe" : [util], 
		"noArgWithPipe" : [printCmd, logFromStdin, "|", util, "-f", "5"]
	}
	return args[key]
'''

'''
Positive tests
'''

'''
@pytest.mark.parametrize("args", 
	[
		getArgs("validArgNoPipe"),
		getArgs("validArgWithPipe")
	]
)
def test_providingValidFileAsArgumentAlwaysReadsFromThatFile(args, expectedValuesReadingFromArg): 
	#Tests reading in a log based on the positional argument FILE
	#Also verifies that util.py defaults to FILE if both a valid FILE and stdin are provided
	
	expected_stdout, expected_stderr, expected_returncode = expectedValuesReadingFromArg
	#actual_stdout, actual_stderr, actual_returncode = runUtil(args)
	actual_stdout, actual_stderr = runUtil(args)
	assert actual_stdout == expected_stdout
	assert actual_stderr == expected_stderr
	#assert actual_returncode == expected_returncode
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

'''
def test_readingFromStdin(expectedValuesReadingFromStdin): 
	#Tests reading in a log from stdin
	
	expected_stdout, expected_stderr, expected_returncode = expectedValuesReadingFromStdin
	#actual_stdout, actual_stderr, actual_returncode = runUtil(getArgs("noArgWithPipe"))
	actual_stdout, actual_stderr = runUtil(getArgs("noArgWithPipe"))
	assert actual_stdout == expected_stdout
	assert actual_stderr == expected_stderr
	#assert actual_returncode == expected_returncode
'''

def test_noArgWithStdin(capsys, monkeypatch, expectedValuesReadingFromStdin): 
	monkeypatch.setattr(sys, "stdin", io.StringIO(expectedValuesReadingFromStdin[0]))
	args = ["-f","5"]
	util.main(args)
	captured = capsys.readouterr()
	expected_stdout, expected_stderr = expectedValuesReadingFromStdin
	assert captured.out == expected_stdout
	assert captured.err == expected_stderr

'''
def test_monkey(monkeypatch, capsys): 
	monkeypatch.setattr(sys, "stdin", io.StringIO('from stdin'))
	util.main(["-f","5"])
	captured = capsys.readouterr()
	assert captured.out == "from stdin"
	assert captured.err == ""
'''

'''
Negative tests
'''

'''
@pytest.mark.parametrize("args", 
	[
		getArgs("invalidArgNoPipe"),
		getArgs("invalidArgWithPipe")
	]
)
def test_errorHandlingForInvalidFileAsArgument(args, expectedValuesForInvalidFile): 
	#Tests error handling when an invalid FILE argument is given
	
	expected_stdout, expected_stderr, expected_returncode = expectedValuesForInvalidFile
	#actual_stdout, actual_stderr, actual_returncode = runUtil(args)
	actual_stdout, actual_stderr = runUtil(args)
	assert actual_stdout == expected_stdout
	assert actual_stderr == expected_stderr
	#assert actual_returncode == expected_returncode
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

'''
def test_errorHandlingForNoInputLogProvided(expectedValuesForNoInput): 
	#Tests error handling when neither FILE nor stdin are provided
	
	expected_stdout, expected_stderr, expected_returncode = expectedValuesForNoInput
	#actual_stdout, actual_stderr, actual_returncode = runUtil(getArgs("noArgNoPipe"))
	actual_stdout, actual_stderr = runUtil(getArgs("noArgNoPipe"))
	assert actual_stdout == expected_stdout
	assert actual_stderr == expected_stderr
	#assert actual_returncode == expected_returncode
'''

def test_noArgNoStdin(expectedValuesForNoInput): 
	'''
	args = ["-f","5"]
	with pytest.raises(SystemExit): 
		util.main(args)
	captured = capsys.readouterr()
	expected_stdout, expected_stderr = expectedValuesForNoInput
	assert captured.out == expected_stdout
	assert captured.err == expected_stderr
	'''
	args = ["-f","5"]
	with pytest.raises(SystemExit): 
		util.main(args)


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
