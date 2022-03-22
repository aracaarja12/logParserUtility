import pytest
import re
import subprocess

'''
Fixtures containing expected values of the form (stdout, stderr, returncode)
'''

@pytest.fixture
def expectedValuesReadingFromArg(): 
	return (
		"This is line 1 Reading from argument\n192.168.255.0 This is line 2 1762:0:0:0:0:B03:1:AF18\nThis is line 3 12:24:59\nThis is line 4 256.256.256.0\nThis is line 5 172.16.254.1", 
		"", 
		0
	)

@pytest.fixture
def expectedValuesReadingFromStdin(): 
	return (
		"This is line 1 Reading from stdin\n192.168.255.0 This is line 2 1762:0:0:0:0:B03:1:AF18\nThis is line 3 12:24:59\nThis is line 4 256.256.256.0\nThis is line 5 172.16.254.1", 
		"", 
		0
	)

@pytest.fixture
def expectedValuesForInvalidFile(): 
	return (
		"",
		"usage: util.py [-h] [-f NUM] [-l NUM] [-t] [-i] [-I] [FILE]\nutil.py: error: argument FILE: can't open 'testLogs\\invalid.log': [Errno 2] No such file or directory: 'testLogs\\\\invalid.log'\n", 
		2
	)

@pytest.fixture
def expectedValuesForNoInput(): 
	return (
		"", 
		"usage: util.py [-h] [-f NUM] [-l NUM] [-t] [-i] [-I] [FILE]\nutil.py: error: A file or standard input must be provided\n", 
		2
	)

'''
Helper functions
'''

def runUtil(args): 
	'''
	Function runs util.py with the given arguments and returns (stdout, stderr, returncode)
	'''
	
	process = subprocess.run(args,capture_output=True,shell=True)
	
	# Decode and standardize stdout
	out = process.stdout.decode("utf-8")
	out = re.sub("\r","",out)
	
	# Decode and standardize stderr
	err = process.stderr.decode("utf-8")
	err = re.sub("\r","",err)
	
	return (out, err, process.returncode)

def getArgs(key): 
	'''
	Function fetches arguments for util.py from a dictionary
	'''
	
	args = {
		"validArgNoPipe" : ["..\\util.py", "-f", "5", "testLogs\\test_input_fromArg.log"], 
		"validArgWithPipe" : ["type", "testLogs\\test_input_fromStdin.log", "|", "..\\util.py", "-f", "5", "testLogs\\test_input_fromArg.log"],  
		"invalidArgNoPipe" : ["..\\util.py", "testLogs\\invalid.log"], 
		"invalidArgWithPipe" : ["type", "testLogs\\test_input_fromStdin.log", "|", "..\\util.py", "testLogs\\invalid.log"], 
		"noArgNoPipe" : ["..\\util.py"], 
		"noArgWithPipe" : ["type", "testLogs\\test_input_fromStdin.log", "|", "..\\util.py", "-f", "5"]
	}
	return args[key]

'''
Positive tests
'''

@pytest.mark.parametrize("args", 
	[
		getArgs("validArgNoPipe"),
		getArgs("validArgWithPipe")
	]
)
def test_providingValidFileAsArgumentAlwaysReadsFromThatFile(args, expectedValuesReadingFromArg): 
	'''
	Tests reading in a log based on the positional argument FILE
	Also verifies that util.py defaults to FILE if both a valid FILE and stdin are provided
	'''
	
	expected_stdout, expected_stderr, expected_returncode = expectedValuesReadingFromArg
	actual_stdout, actual_stderr, actual_returncode = runUtil(args)
	assert actual_stdout == expected_stdout
	assert actual_stderr == expected_stderr
	assert actual_returncode == expected_returncode

def test_readingFromStdin(expectedValuesReadingFromStdin): 
	'''
	Tests reading in a log from stdin
	'''
	
	expected_stdout, expected_stderr, expected_returncode = expectedValuesReadingFromStdin
	actual_stdout, actual_stderr, actual_returncode = runUtil(getArgs("noArgWithPipe"))
	assert actual_stdout == expected_stdout
	assert actual_stderr == expected_stderr
	assert actual_returncode == expected_returncode

'''
Negative tests
'''

@pytest.mark.parametrize("args", 
	[
		getArgs("invalidArgNoPipe"),
		getArgs("invalidArgWithPipe")
	]
)
def test_errorHandlingForInvalidFileAsArgument(args, expectedValuesForInvalidFile): 
	'''
	Tests error handling when an invalid FILE argument is given
	'''
	
	expected_stdout, expected_stderr, expected_returncode = expectedValuesForInvalidFile
	actual_stdout, actual_stderr, actual_returncode = runUtil(args)
	assert actual_stdout == expected_stdout
	assert actual_stderr == expected_stderr
	assert actual_returncode == expected_returncode

def test_errorHandlingForNoInputLogProvided(expectedValuesForNoInput): 
	'''
	Tests error handling when neither FILE nor stdin are provided
	'''
	
	expected_stdout, expected_stderr, expected_returncode = expectedValuesForNoInput
	actual_stdout, actual_stderr, actual_returncode = runUtil(getArgs("noArgNoPipe"))
	assert actual_stdout == expected_stdout
	assert actual_stderr == expected_stderr
	assert actual_returncode == expected_returncode

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
