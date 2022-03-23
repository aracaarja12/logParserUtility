import pytest
import sys
import os
from pathlib import PurePath
import subprocess

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import util

'''
Fixtures
'''

@pytest.fixture
def timestampLog(): 
	'''
	Returns the text of testLogs/test_timestamp.log
	'''
	
	return (
		"Line 1 04:06:15 valid\n",
		"Line 2 4:06:15 invalid\n",
		"14:59:06 Line 3 valid\n",
		"Line 4 14:70:06 invalid\n",
		"Line 5 valid 18:30:24\n",
		"Line 6 20:30 invalid\n",
		"Line 7 valid 23:59:59\n",
		"Line 8 invalid 20:04:100\n",
		"Line 9 valid 00:00:00\n",
		"Line 10 invalid00:04:10\n"
	)

@pytest.fixture
def ipv4Log(): 
	'''
	Returns the text of testLogs/test_ipv4.log
	'''
	
	return (
		"Line 1 192.168.255.0 valid\n",
		"Line 2 192.260.255.0 invalid\n",
		"86.115.8.11 Line 3 valid\n",
		"Line 4 234.98.125.251invalid\n",
		"Line 5 valid 234.098.125.251\n",
		"Line 6234.98.125.251 invalid\n",
		"Line 7 valid 0.0.0.0\n",
		"Line 8 invalid 43.119.240.-72\n",
		"Line 9 valid 255.255.255.255\n",
		"Line 10 invalid 331.101.157"
	)

@pytest.fixture
def ipv6Log(): 
	'''
	Returns the text of testLogs/test_ipv6.log
	'''
	
	return (
		"Line 1 cc13:467e:88db:a4b0:fc68:dd9d:5a9e:ab80 valid\n",
		"Line 2 cc13:467e:88db:a4b0:fc68:dd9d:5a9e invalid\n",
		"CF91:B4ED:13FB:1857:6B32:CB99:54E8:82BC Line 3 valid\n",
		"Line 4 cc13:467e:88db:a4b0:fc68:dd9d:5a9e:ab80invalid\n",
		"Line 5 valid Cf91:B4Ed:13Fb:1857:6B32:cB99:54e8:82Bc\n",
		"Line 6cc13:467e:88db:a4b0:fc68:dd9d:5a9e:ab80 invalid\n",
		"Line 7 valid 2bc2:2a2d:98:dc3:0:18e0:aa7c:c0bd\n",
		"Line 8 invalid cc13:467e:88db:a4b0000:fc68:dd9d:5a9e:ab80\n",
		"Line 9 valid FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF\n",
		"Line 10 invalid cc13:467e:88dG:a4b0:fc68:dd9d:5a9e:ab80"
	)

'''
Helpers
'''

def getExpectedLines(logText,idx): 
	'''
	Returns expected text from the given log based on a list of lines that should be printed
	'''
	
	return "".join([logText[i] for i in idx if i < len(logText)  and i >= 0])

def getExpectedValuesForErroneousArgs(extraArg): 
	'''
	Returns values of the form (stdout, stderr) for when an argument is erroneously supplied to -t, -i, or -I
	'''
	
	scriptName = PurePath(sys.argv[0]).parts[-1]
	return (
		"",
		f"usage: {scriptName} [-h] [-f NUM] [-l NUM] [-t] [-i] [-I] [FILE]\n{scriptName}: error: unrecognized arguments: {extraArg}\n"
	)

'''
Positive tests
'''

@pytest.mark.parametrize("switch", ["-t","--timestamp"])
def test_timestampOnly(capsys, timestampLog, switch): 
	'''
	Tests -t independently with a log containing valid and invalid timestamps (valid timestamps are of the form HH:MM:SS)
	'''
	
	args = [switch,"testLogs/test_timestamp.log"]
	util.main(args)
	captured = capsys.readouterr()
	expected = getExpectedLines(timestampLog,[i for i in range(0,10,2)])
	assert captured.out == expected
	assert captured.err == ""

@pytest.mark.parametrize("switch", ["-i","--ipv4"])
def test_ipv4Only(capsys, ipv4Log, switch): 
	'''
	Tests -i independently with a log containing valid and invalid IPv4 addresses (valid IPs are of the form xxx.xxx.xxx.xxx where xxx is in (0,255))
	Note: this does not verify IP highlighting
	'''
	
	args = [switch,"testLogs/test_ipv4.log"]
	util.main(args)
	captured = capsys.readouterr()
	expected = getExpectedLines(ipv4Log,[i for i in range(0,10,2)])
	assert captured.out == expected
	assert captured.err == ""

@pytest.mark.parametrize("switch", ["-I","--ipv6"])
def test_ipv6Only(capsys, ipv6Log, switch): 
	'''
	Tests -I independently with a log containing valid and invalid IPv6 addresses (valid IPs are of the form yyyy:yyyy:yyyy:yyyy:yyyy:yyyy:yyyy:yyyy where y is in hex (0-F))
	Note: this does not verify IP highlighting
	'''
	
	args = [switch,"testLogs/test_ipv6.log"]
	util.main(args)
	captured = capsys.readouterr()
	expected = getExpectedLines(ipv6Log,[i for i in range(0,10,2)])
	assert captured.out == expected
	assert captured.err == ""

'''
Negative tests
'''

@pytest.mark.parametrize("option", ["-t","-i","-I"])
def test_timestampAndIPOptionsDoNotTakeArgs(capsys, option): 
	'''
	Tests error handling when user tries to supply an argument to -t, -i, or -I
	'''
	
	extraArg = 5
	args = ["testLogs/test_timestamp.log",option,str(extraArg)]
	with pytest.raises(SystemExit): 
		util.main(args)
	captured = capsys.readouterr()
	expected_stdout, expected_stderr = getExpectedValuesForErroneousArgs(extraArg)
	assert captured.out == expected_stdout
	assert captured.err == expected_stderr


'''
args = ["..\\util.py","-i","testLogs/test_ipv4.log"]
output = subprocess.run(args,capture_output=True,shell=True)
so = output.stdout.decode("utf-8")
se = output.stderr.decode("utf-8")
sn = output.returncode

print(repr(so))
print(repr(se))
print(repr(sn))
'''


