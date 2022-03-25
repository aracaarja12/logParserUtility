import pytest
import sys
import os
from pathlib import PurePath

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import util

'''
Helpers
'''

'''
def get_expected_lines(log_text, idx): 
	#Returns expected text from the given log based on a list of lines that should be printed
	
	return "".join([log_text[i] for i in idx if i < len(log_text)  and i >= 0])
'''

def get_expected_values_for_erroneous_args(extra_arg): 
	'''
	Returns values of the form (stdout, stderr) for when an argument is erroneously supplied to -t, -i, or -I
	'''
	
	script_name = PurePath(sys.argv[0]).parts[-1]
	return (
		"",
		f"usage: {script_name} [-h] [-f NUM] [-l NUM] [-t] [-i] [-I] [FILE]\n{script_name}: error: unrecognized arguments: {extra_arg}\n"
	)

'''
Positive tests
'''

def test_timestamp_only(capsys): 
	'''
	Tests -t independently with a log containing valid and invalid timestamps (valid timestamps are of the form HH:MM:SS)
	'''
	
	args = ["--timestamp", "testLogs/test_timestamp.log"]
	util.main(args)
	captured = capsys.readouterr()
	expected = "Line 1 04:06:15 valid\n14:59:06 Line 3 valid\nLine 5 valid 18:30:24\nLine 7 valid 23:59:59\nLine 9 valid 00:00:00\n12:05:35 22:59:05 00:03:12"
	assert captured.out == expected
	assert captured.err == ""

def test_ipv4_only(capsys): 
	'''
	Tests -i independently with a log containing valid and invalid IPv4 addresses (valid IPs are of the form xxx.xxx.xxx.xxx where xxx is in (0,255))
	Note: this does not verify IP highlighting
	'''
	
	args = ["--ipv4", "testLogs/test_ipv4.log"]
	util.main(args)
	captured = capsys.readouterr()
	expected = "Line 1 192.168.255.0 valid\n86.115.8.11 Line 3 valid\nLine 5 valid 234.098.125.251\nLine 7 valid 0.0.0.0\nLine 9 valid 255.255.255.255\n192.168.255.0 86.115.8.11 43.119.240.72"
	assert captured.out == expected
	assert captured.err == ""

def test_ipv6_only(capsys): 
	'''
	Tests -I independently with a log containing valid and invalid IPv6 addresses (valid IPs are of the form yyyy:yyyy:yyyy:yyyy:yyyy:yyyy:yyyy:yyyy where y is in hex (0-F))
	Note: this does not verify IP highlighting
	'''
	
	args = ["--ipv6", "testLogs/test_ipv6.log"]
	util.main(args)
	captured = capsys.readouterr()
	expected = "Line 1 cc13:467e:88db:a4b0:fc68:dd9d:5a9e:ab80 valid\nCF91:B4ED:13FB:1857:6B32:CB99:54E8:82BC Line 3 valid\nLine 5 valid Cf91:B4Ed:13Fb:1857:6B32:cB99:54e8:82Bc\nLine 7 valid 2bc2:2a2d:98:dc3:0:18e0:aa7c:c0bd\nLine 9 valid FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF\n2bc2:2a2d:98:dc3:0:18e0:aa7c:c0bd cc13:467e:88db:a4b0:fc68:dd9d:5a9e:ab80 0000:0000:0000:0000:0000:0000:0000:0000"
	assert captured.out == expected
	assert captured.err == ""

def test_timestamp_and_ipv4(capsys): 
	'''
	Tests -t in conjunction with -i
	'''
	
	args = ["-t", "-i", "testLogs/test_general.log"]
	util.main(args)
	captured = capsys.readouterr()
	expected = "Line 2: 02:49:12 172.16.254.1 ti\nLine 3: 192.168.255.0 02:38:00 127.0.0.1 ti\nLine 5: 127.255.0.10 23:59:59 192.168.255.255 0aF3:AF18:1762:B03:0:1:af19:17f tiI\nLine 12: 00:000:00:000:00:000:00:00 0.0.0.0 00:00:00 tiI\nLine 13: 09:17:17 : 2bc2:2a2d:98:dc3:0:18e0:aa7c:c0bd -- 234.098.125.251 200 tiI\nLine 15: 127.127.127.127 abcd:1234:ab:12:abcd:1234:cd:34 03:01:56 tiI\nLine 17: 119.243.4.69 88.133.63.210 17:59:00 17c8:d4ea:1cb2:afeb:d2b9:945e:6e6e:9152 tiI\nLine 20: 04:52:24 144.1.18.87 ti"
	assert captured.out == expected
	assert captured.err == ""

def test_timestamp_and_ipv6(capsys): 
	args = ["-t", "-I", "testLogs/test_general.log"]
	util.main(args)
	captured = capsys.readouterr()
	expected = "Line 5: 127.255.0.10 23:59:59 192.168.255.255 0aF3:AF18:1762:B03:0:1:af19:17f tiI\nLine 9: Cf91:B4Ed:13Fb:1857:6B32:cB99:54e8:82Bc 00:00:00 2bc2:2a2d:98:dc3:0:18e0:aa7c:c0bd tI\nLine 10: cc13:467e:88db:a4b0:fc68:dd9d:5a9e:ab80 06:15:04 tI\nLine 12: 00:000:00:000:00:000:00:00 0.0.0.0 00:00:00 tiI\nLine 13: 09:17:17 : 2bc2:2a2d:98:dc3:0:18e0:aa7c:c0bd -- 234.098.125.251 200 tiI\nLine 15: 127.127.127.127 abcd:1234:ab:12:abcd:1234:cd:34 03:01:56 tiI\nLine 17: 119.243.4.69 88.133.63.210 17:59:00 17c8:d4ea:1cb2:afeb:d2b9:945e:6e6e:9152 tiI\nLine 19: f3ba:559b:77b1:8fd6:d46c:ffc8:dc92:5f7c 14:25:42 tI\n"
	assert captured.out == expected
	assert captured.err == ""

def test_ipv4_and_ipv6(capsys): 
	args = ["-i", "-I", "testLogs/test_general.log"]
	util.main(args)
	captured = capsys.readouterr()
	expected = "Line 5: 127.255.0.10 23:59:59 192.168.255.255 0aF3:AF18:1762:B03:0:1:af19:17f tiI\nLine 12: 00:000:00:000:00:000:00:00 0.0.0.0 00:00:00 tiI\nLine 13: 09:17:17 : 2bc2:2a2d:98:dc3:0:18e0:aa7c:c0bd -- 234.098.125.251 200 tiI\nLine 14: 2bc2:2a2d:98:dc3:0:18e0:aa7c:c0bd -- 234.098.125.251 200 iI\nLine 15: 127.127.127.127 abcd:1234:ab:12:abcd:1234:cd:34 03:01:56 tiI\nLine 16: 6a03:b896:63fd:c4a2:92d8:16d6:99bf:b429 37.196.62.32 iI\nLine 17: 119.243.4.69 88.133.63.210 17:59:00 17c8:d4ea:1cb2:afeb:d2b9:945e:6e6e:9152 tiI\nLine 18: 162.181.128.181 28e4:aaa0:54f4:2de6:dc4a:916f:7cb8:b541 iI\n"
	assert captured.out == expected
	assert captured.err == ""

def test_timestamp_and_ipv4_and_ipv6(capsys): 
	args = ["-t", "-i", "-I", "testLogs/test_general.log"]
	util.main(args)
	captured = capsys.readouterr()
	expected = "Line 5: 127.255.0.10 23:59:59 192.168.255.255 0aF3:AF18:1762:B03:0:1:af19:17f tiI\nLine 12: 00:000:00:000:00:000:00:00 0.0.0.0 00:00:00 tiI\nLine 13: 09:17:17 : 2bc2:2a2d:98:dc3:0:18e0:aa7c:c0bd -- 234.098.125.251 200 tiI\nLine 15: 127.127.127.127 abcd:1234:ab:12:abcd:1234:cd:34 03:01:56 tiI\nLine 17: 119.243.4.69 88.133.63.210 17:59:00 17c8:d4ea:1cb2:afeb:d2b9:945e:6e6e:9152 tiI\n"
	assert captured.out == expected
	assert captured.err == ""

# TODO add coverage for -f and -l combined with some combination of -t, -i, and -I

# TODO add coverage for IP highlighting (ie unit tests for highlight_ip_addresses())

# TODO add unit tests for split_by_idx

'''
Negative tests
'''

@pytest.mark.parametrize("option", ["-t", "-i", "-I"])
def test_timestamp_and_ip_options_do_not_take_args(capsys, option): 
	'''
	Tests error handling when user tries to supply an argument to -t, -i, or -I
	'''
	
	extra_arg = 5
	args = ["testLogs/test_timestamp.log", option, str(extra_arg)]
	with pytest.raises(SystemExit): 
		util.main(args)
	captured = capsys.readouterr()
	expected_stdout, expected_stderr = get_expected_values_for_erroneous_args(extra_arg)
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


