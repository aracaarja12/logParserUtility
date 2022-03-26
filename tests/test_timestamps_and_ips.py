import pytest
import sys
import os
import re

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import util

general_log = "testLogs/test_general.log"
timestamp_log = "testLogs/test_timestamp.log"
ipv4_log = "testLogs/test_ipv4.log"
ipv6_log = "testLogs/test_ipv6.log"

class TestPositive: 

    @pytest.mark.functional
    def test_timestamp_only(self, capsys): 
        '''
        Tests -t with a log containing valid and invalid timestamps
        Valid timestamps are of the form HH:MM:SS
        '''
        
        args = ["--timestamp", timestamp_log]
        util.main(args)
        captured = capsys.readouterr()
        expected = (
            "Line 1 04:06:15 valid\n14:59:06 Line 3 valid\nLine 5 valid "
            "18:30:24\nLine 7 valid 23:59:59\nLine 9 valid 00:00:00\n12:05:35 "
            "22:59:05 00:03:12"
        )
        assert captured.out == expected
        assert captured.err == ""

    @pytest.mark.functional
    def test_ipv4_only(self, capsys): 
        '''
        Tests -i with a log containing valid and invalid IPv4 addresses
        Valid IPv4s are of the form 
            xxx.xxx.xxx.xxx
            where xxx is in (0,255)
            and leading 0s are optional
        '''
        
        args = ["--ipv4", ipv4_log]
        util.main(args)
        captured = capsys.readouterr()
        expected = (
            "Line 1 192.168.255.0 valid\n86.115.8.11 Line 3 valid\nLine 5 "
            "valid 234.098.125.251\nLine 7 valid 0.0.0.0\nLine 9 valid "
            "255.255.255.255\n192.168.255.0 86.115.8.11 43.119.240.72"
        )
        assert captured.out == expected
        assert captured.err == ""

    @pytest.mark.functional
    def test_ipv6_only(self, capsys): 
        '''
        Tests -I with a log containing valid and invalid IPv6 addresses
        Valid IPv6s are of the form 
            yyyy:yyyy:yyyy:yyyy:yyyy:yyyy:yyyy:yyyy 
            where y is in hex (0-F))
            and leading 0s are optional
        '''
        
        args = ["--ipv6", ipv6_log]
        util.main(args)
        captured = capsys.readouterr()
        expected = (
            "Line 1 cc13:467e:88db:a4b0:fc68:dd9d:5a9e:ab80 valid\nCF91:B4ED:"
            "13FB:1857:6B32:CB99:54E8:82BC Line 3 valid\nLine 5 valid Cf91:"
            "B4Ed:13Fb:1857:6B32:cB99:54e8:82Bc\nLine 7 valid 2bc2:2a2d:98:"
            "dc3:0:18e0:aa7c:c0bd\nLine 9 valid FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:"
            "FFFF:FFFF\n2bc2:2a2d:98:dc3:0:18e0:aa7c:c0bd cc13:467e:88db:a4b0:"
            "fc68:dd9d:5a9e:ab80 0000:0000:0000:0000:0000:0000:0000:0000"
        )
        assert captured.out == expected
        assert captured.err == ""

    @pytest.mark.functional
    def test_timestamp_and_ipv4(self, capsys): 
        '''
        Tests -t in conjunction with -i
        '''
        
        args = ["-t", "-i", general_log]
        util.main(args)
        captured = capsys.readouterr()
        expected = (
            "Line 2: 02:49:12 172.16.254.1 ti\nLine 3: 192.168.255.0 02:38:00 "
            "127.0.0.1 ti\nLine 5: 127.255.0.10 23:59:59 192.168.255.255 0aF3:"
            "AF18:1762:B03:0:1:af19:17f tiI\nLine 12: 00:000:00:000:00:000:00:"
            "00 0.0.0.0 00:00:00 tiI\nLine 13: 09:17:17 : 2bc2:2a2d:98:dc3:0:"
            "18e0:aa7c:c0bd -- 234.098.125.251 200 tiI\nLine 15: 127.127.127."
            "127 abcd:1234:ab:12:abcd:1234:cd:34 03:01:56 tiI\nLine 17: 119."
            "243.4.69 88.133.63.210 17:59:00 17c8:d4ea:1cb2:afeb:d2b9:945e:"
            "6e6e:9152 tiI\nLine 20: 04:52:24 144.1.18.87 ti"
        )
        assert captured.out == expected
        assert captured.err == ""

    @pytest.mark.functional
    def test_timestamp_and_ipv6(self, capsys): 
        '''
        Tests -t in conjunction with -I
        '''
        
        args = ["-t", "-I", general_log]
        util.main(args)
        captured = capsys.readouterr()
        expected = (
            "Line 5: 127.255.0.10 23:59:59 192.168.255.255 0aF3:AF18:1762:B03:"
            "0:1:af19:17f tiI\nLine 9: Cf91:B4Ed:13Fb:1857:6B32:cB99:54e8:"
            "82Bc 00:00:00 2bc2:2a2d:98:dc3:0:18e0:aa7c:c0bd tI\nLine 10: "
            "cc13:467e:88db:a4b0:fc68:dd9d:5a9e:ab80 06:15:04 tI\nLine 12: 00:"
            "000:00:000:00:000:00:00 0.0.0.0 00:00:00 tiI\nLine 13: 09:17:17 "
            ": 2bc2:2a2d:98:dc3:0:18e0:aa7c:c0bd -- 234.098.125.251 200 tiI\n"
            "Line 15: 127.127.127.127 abcd:1234:ab:12:abcd:1234:cd:34 03:01:"
            "56 tiI\nLine 17: 119.243.4.69 88.133.63.210 17:59:00 17c8:d4ea:"
            "1cb2:afeb:d2b9:945e:6e6e:9152 tiI\nLine 19: f3ba:559b:77b1:8fd6:"
            "d46c:ffc8:dc92:5f7c 14:25:42 tI\n"
        )
        assert captured.out == expected
        assert captured.err == ""

    @pytest.mark.functional
    def test_ipv4_and_ipv6(self, capsys): 
        '''
        Tests -i in conjunction with -I
        '''
        
        args = ["-i", "-I", general_log]
        util.main(args)
        captured = capsys.readouterr()
        expected = (
            "Line 5: 127.255.0.10 23:59:59 192.168.255.255 0aF3:AF18:1762:B03:"
            "0:1:af19:17f tiI\nLine 12: 00:000:00:000:00:000:00:00 0.0.0.0 00:"
            "00:00 tiI\nLine 13: 09:17:17 : 2bc2:2a2d:98:dc3:0:18e0:aa7c:c0bd "
            "-- 234.098.125.251 200 tiI\nLine 14: 2bc2:2a2d:98:dc3:0:18e0:"
            "aa7c:c0bd -- 234.098.125.251 200 iI\nLine 15: 127.127.127.127 "
            "abcd:1234:ab:12:abcd:1234:cd:34 03:01:56 tiI\nLine 16: 6a03:b896:"
            "63fd:c4a2:92d8:16d6:99bf:b429 37.196.62.32 iI\nLine 17: 119.243.4"
            ".69 88.133.63.210 17:59:00 17c8:d4ea:1cb2:afeb:d2b9:945e:6e6e:"
            "9152 tiI\nLine 18: 162.181.128.181 28e4:aaa0:54f4:2de6:dc4a:916f:"
            "7cb8:b541 iI\n"
        )
        assert captured.out == expected
        assert captured.err == ""

    @pytest.mark.functional
    def test_timestamp_and_ipv4_and_ipv6(self, capsys): 
        '''
        Tests -t, -i, and -I together
        '''
        
        args = ["-t", "-i", "-I", general_log]
        util.main(args)
        captured = capsys.readouterr()
        expected = (
            "Line 5: 127.255.0.10 23:59:59 192.168.255.255 0aF3:AF18:1762:B03:"
            "0:1:af19:17f tiI\nLine 12: 00:000:00:000:00:000:00:00 0.0.0.0 00:"
            "00:00 tiI\nLine 13: 09:17:17 : 2bc2:2a2d:98:dc3:0:18e0:aa7c:c0bd "
            "-- 234.098.125.251 200 tiI\nLine 15: 127.127.127.127 abcd:1234:"
            "ab:12:abcd:1234:cd:34 03:01:56 tiI\nLine 17: 119.243.4.69 88.133."
            "63.210 17:59:00 17c8:d4ea:1cb2:afeb:d2b9:945e:6e6e:9152 tiI\n"
        )
        assert captured.out == expected
        assert captured.err == ""

    @pytest.mark.functional
    def test_first_with_all_timestamp_and_ip_options(self, capsys): 
        '''
        Tests -f, -t, -i, and -I together
        '''
        
        args = ["-t", "-i", "-I", "-f", "13", general_log]
        util.main(args)
        captured = capsys.readouterr()
        expected = (
            "Line 5: 127.255.0.10 23:59:59 192.168.255.255 0aF3:AF18:1762:B03:"
            "0:1:af19:17f tiI\nLine 12: 00:000:00:000:00:000:00:00 0.0.0.0 00:"
            "00:00 tiI\nLine 13: 09:17:17 : 2bc2:2a2d:98:dc3:0:18e0:aa7c:c0bd "
            "-- 234.098.125.251 200 tiI\n"
        )
        assert captured.out == expected
        assert captured.err == ""

    @pytest.mark.functional
    def test_last_with_all_timestamp_and_ip_options(self, capsys):
        '''
        Tests -l, -t, -i, and -I together
        '''
        
        args = ["-t", "-i", "-I", "-l", "13", general_log]
        util.main(args)
        captured = capsys.readouterr()
        expected = (
            "Line 12: 00:000:00:000:00:000:00:00 0.0.0.0 00:00:00 tiI\nLine "
            "13: 09:17:17 : 2bc2:2a2d:98:dc3:0:18e0:aa7c:c0bd -- 234.098.125."
            "251 200 tiI\nLine 15: 127.127.127.127 abcd:1234:ab:12:abcd:1234:"
            "cd:34 03:01:56 tiI\nLine 17: 119.243.4.69 88.133.63.210 17:59:00 "
            "17c8:d4ea:1cb2:afeb:d2b9:945e:6e6e:9152 tiI\n"
        )
        assert captured.out == expected
        assert captured.err == ""

    @pytest.mark.functional
    def test_first_and_last_with_all_timestamp_and_ip_options(self, capsys): 
        '''
        Tests -f, -l, -t, -i, and -I together
        '''
        
        args = ["-t", "-i", "-I", "-f", "13", "-l", "13", general_log]
        util.main(args)
        captured = capsys.readouterr()
        expected = (
            "Line 12: 00:000:00:000:00:000:00:00 0.0.0.0 00:00:00 tiI\nLine "
            "13: 09:17:17 : 2bc2:2a2d:98:dc3:0:18e0:aa7c:c0bd -- 234.098.125."
            "251 200 tiI\n"
        )
        assert captured.out == expected
        assert captured.err == ""

    @pytest.mark.unit
    def test_ip_highlighting(self): 
        '''
        Tests IP address highlighting
        '''
        
        input = (
            "119.243.4.69 54ad:92fb:9c62:dcc1:39fb:d679:73f4:b804 88.133.63."
            "210 17:59:00 17c8:d4ea:1cb2:afeb:d2b9:945e:6e6e:9152"
        )
        ipv4_re = re.compile(
            (
                r"\b(([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\.){3}([01]?[0-9][0"
                r"-9]?|2[0-4][0-9]|25[0-5])\b"
            )
        )
        ipv6_re = re.compile(
            r"\b([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b"
        )
        
        # Verifies IPv6 highlighting
        matches = ipv6_re.finditer(input)
        actual = util.highlight_ip_addresses(input, matches)
        expected = (
            "119.243.4.69 \x1b[42m54ad:92fb:9c62:dcc1:39fb:d679:73f4:b804\x1b["
            "0m 88.133.63.210 17:59:00 \x1b[42m17c8:d4ea:1cb2:afeb:d2b9:945e:"
            "6e6e:9152\x1b[0m"
        )
        assert actual == expected
        
        # Verifies IPv4 highlighting
        matches = ipv4_re.finditer(input)
        actual = util.highlight_ip_addresses(input, matches)
        expected = (
            "\x1b[42m119.243.4.69\x1b[0m 54ad:92fb:9c62:dcc1:39fb:d679:73f4:"
            "b804 \x1b[42m88.133.63.210\x1b[0m 17:59:00 17c8:d4ea:1cb2:afeb:"
            "d2b9:945e:6e6e:9152"
        )
        assert actual == expected
        
        # Verifies the highlighting of an already-highlighted string
        input = actual
        matches = ipv6_re.finditer(input)
        actual = util.highlight_ip_addresses(input, matches)
        expected = (
            "\x1b[42m119.243.4.69\x1b[0m \x1b[42m54ad:92fb:9c62:dcc1:39fb:"
            "d679:73f4:b804\x1b[0m \x1b[42m88.133.63.210\x1b[0m 17:59:00 \x1b"
            "[42m17c8:d4ea:1cb2:afeb:d2b9:945e:6e6e:9152\x1b[0m"
        )
        assert actual == expected

    @pytest.mark.unit
    def test_split_by_idx(self): 
        '''
        Tests the util.split_by_idx() generator
        '''
        
        input = "I'm gonna take my horse to the old town road"
        idx = [4, 9, 31]
        actual = [*util.split_by_idx(input,idx)]
        expected = ["I'm ", "gonna", " take my horse to the ", "old town road"]
        assert actual == expected

class TestNegative: 

    @staticmethod
    def get_expected_values_for_erroneous_args(script_name, extra_arg): 
        '''
        Returns expected (stdout, stderr) when an argument is 
            erroneously supplied to -t, -i, or -I
        '''
        
        return (
            "",
            (
                f"usage: {script_name} [-h] [-f NUM] [-l NUM] [-t] [-i] [-I] "
                f"[FILE]\n{script_name}: error: unrecognized arguments: "
                f"{extra_arg}\n"
            )
        )

    @pytest.mark.parametrize("option", ["-t", "-i", "-I"])
    def test_timestamp_and_ip_options_do_not_take_args(
            self, capsys, script_name, option): 
        '''
        Tests error handling when user tries to supply an argument to 
            -t, -i, or -I
        '''
        
        extra_arg = 5
        args = [timestamp_log, option, str(extra_arg)]
        with pytest.raises(SystemExit): 
            util.main(args)
        captured = capsys.readouterr()
        expected_stdout, expected_stderr = (
            self.get_expected_values_for_erroneous_args(script_name, extra_arg)
        )
        assert captured.out == expected_stdout
        assert captured.err == expected_stderr
