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
def log_from_arg(): 
	return str(PurePath("testLogs/test_input_from_arg.log"))

@pytest.fixture
def log_from_stdin(): 
	return str(PurePath("testLogs/test_input_from_stdin.log"))

@pytest.fixture
def invalid_log(): 
	return "invalid.log"

@pytest.fixture
def util_script(): 
	return str(PurePath("../util.py"))

'''
Fixtures that return expected values of the form (stdout, stderr)
'''

@pytest.fixture
def expected_values_reading_from_arg(): 
	return (
		"This is line 1 Reading from argument\n192.168.255.0 This is line 2 1762:0:0:0:0:B03:1:AF18\nThis is line 3 12:24:59\nThis is line 4 256.256.256.0\nThis is line 5 172.16.254.1", 
		""
	)

@pytest.fixture
def expected_values_reading_from_stdin(): 
	return (
		"This is line 1 Reading from stdin\n192.168.255.0 This is line 2 1762:0:0:0:0:B03:1:AF18\nThis is line 3 12:24:59\nThis is line 4 256.256.256.0\nThis is line 5 172.16.254.1", 
		""
	)

@pytest.fixture
def expected_values_for_invalid_file(invalid_log): 
	scriptName = PurePath(sys.argv[0]).parts[-1]
	return (
		"",
		f"usage: {scriptName} [-h] [-f NUM] [-l NUM] [-t] [-i] [-I] [FILE]\n{scriptName}: error: argument FILE: can't open '{invalid_log}': [Errno 2] No such file or directory: '{invalid_log}'\n"
	)

@pytest.fixture
def expected_values_for_no_input(): 
	return (
		"", 
		"usage: util.py [-h] [-f NUM] [-l NUM] [-t] [-i] [-I] [FILE]\nutil.py: error: A file or standard input must be provided\n"
	)

'''
Helper functions
'''

def run_util(args): 
	'''
	Function runs util.py with the given arguments and returns (stdout, stderr, returncode)
	'''
	
	process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = process.communicate()
	
	out = out.decode("utf-8")
	out = re.sub("\r", "", out)
	
	err = err.decode("utf-8")
	err = re.sub("\r", "", err)
	
	return (out, err)

'''
Positive tests
'''

def test_valid_arg_no_stdin(capsys, log_from_arg, expected_values_reading_from_arg): 
	args = ["-f", "5", log_from_arg]
	util.main(args)
	captured = capsys.readouterr()
	expected_stdout, expected_stderr = expected_values_reading_from_arg
	assert captured.out == expected_stdout
	assert captured.err == expected_stderr

def test_valid_arg_with_stdin(capsys, monkeypatch, log_from_arg, expected_values_reading_from_stdin, expected_values_reading_from_arg): 
	monkeypatch.setattr(sys, "stdin", io.StringIO(expected_values_reading_from_stdin[0]))
	args = ["-f", "5", log_from_arg]
	util.main(args)
	captured = capsys.readouterr()
	expected_stdout, expected_stderr = expected_values_reading_from_arg
	assert captured.out == expected_stdout
	assert captured.err == expected_stderr

def test_no_arg_with_stdin(capsys, monkeypatch, expected_values_reading_from_stdin): 
	monkeypatch.setattr(sys, "stdin", io.StringIO(expected_values_reading_from_stdin[0]))
	args = ["-f", "5"]
	util.main(args)
	captured = capsys.readouterr()
	expected_stdout, expected_stderr = expected_values_reading_from_stdin
	assert captured.out == expected_stdout
	assert captured.err == expected_stderr

'''
Negative tests
'''

def test_invalid_arg_no_stdin(capsys, invalid_log, expected_values_for_invalid_file): 
	args = ["-f", "5", invalid_log]
	with pytest.raises(SystemExit): 
		util.main(args)
	captured = capsys.readouterr()
	expected_stdout, expected_stderr = expected_values_for_invalid_file
	assert captured.out == expected_stdout
	assert captured.err == expected_stderr

def test_invalid_arg_with_stdin(capsys, monkeypatch, invalid_log, expected_values_reading_from_stdin, expected_values_for_invalid_file): 
	monkeypatch.setattr(sys, "stdin", io.StringIO(expected_values_reading_from_stdin[0]))
	args = ["-f", "5", invalid_log]
	with pytest.raises(SystemExit): 
		util.main(args)
	captured = capsys.readouterr()
	expected_stdout, expected_stderr = expected_values_for_invalid_file
	assert captured.out == expected_stdout
	assert captured.err == expected_stderr

#TODO: delete this
@pytest.mark.xfail
def test_no_arg_no_stdin(util_script, expected_values_for_no_input): 
	args = [util_script]
	actual_stdout, actual_stderr = run_util(args)
	expected_stdout, expected_stderr = expected_values_for_no_input
	assert actual_stdout == expected_stdout
	assert actual_stderr == expected_stderr
