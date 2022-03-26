import pytest
import sys
import os
import io
import re
from pathlib import PurePath

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import util

@pytest.fixture
def expected_values_reading_from_stdin(): 
    return (
        "This is line 1 Reading from stdin\n192.168.255.0 This is line 2 1762:0:0:0:0:B03:1:AF18\nThis is line 3 12:24:59\nThis is line 4 256.256.256.0\nThis is line 5 172.16.254.1", 
        ""
    )

class TestPositive: 

    @pytest.fixture
    def log_from_arg(self): 
        return str(PurePath("testLogs/test_input_from_arg.log"))

    @pytest.fixture
    def expected_values_reading_from_arg(self): 
        return (
            "This is line 1 Reading from argument\n192.168.255.0 This is line 2 1762:0:0:0:0:B03:1:AF18\nThis is line 3 12:24:59\nThis is line 4 256.256.256.0\nThis is line 5 172.16.254.1", 
            ""
        )

    def test_valid_arg_no_stdin(self, capsys, log_from_arg, expected_values_reading_from_arg): 
        args = ["-f", "5", log_from_arg]
        util.main(args)
        captured = capsys.readouterr()
        expected_stdout, expected_stderr = expected_values_reading_from_arg
        assert captured.out == expected_stdout
        assert captured.err == expected_stderr

    def test_valid_arg_with_stdin(self, capsys, monkeypatch, log_from_arg, expected_values_reading_from_stdin, expected_values_reading_from_arg): 
        monkeypatch.setattr(sys, "stdin", io.StringIO(expected_values_reading_from_stdin[0]))
        args = ["-f", "5", log_from_arg]
        util.main(args)
        captured = capsys.readouterr()
        expected_stdout, expected_stderr = expected_values_reading_from_arg
        assert captured.out == expected_stdout
        assert captured.err == expected_stderr

    def test_no_arg_with_stdin(self, capsys, monkeypatch, expected_values_reading_from_stdin): 
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

class TestNegative: 

    @pytest.fixture
    def invalid_log(self): 
        return "invalid.log"

    @pytest.fixture
    def expected_values_for_invalid_file(self, invalid_log): 
        script_name = PurePath(sys.argv[0]).parts[-1]
        return (
            "",
            f"usage: {script_name} [-h] [-f NUM] [-l NUM] [-t] [-i] [-I] [FILE]\n{script_name}: error: argument FILE: can't open '{invalid_log}': [Errno 2] No such file or directory: '{invalid_log}'\n"
        )

    @pytest.fixture
    def expected_values_for_no_input(self): 
        script_name = PurePath(sys.argv[0]).parts[-1]
        return (
            "", 
            f"usage: {script_name} [-h] [-f NUM] [-l NUM] [-t] [-i] [-I] [FILE]\n{script_name}: error: A file or standard input must be provided. Try -h for help.\n"
        )

    def test_invalid_arg_no_stdin(self, capsys, invalid_log, expected_values_for_invalid_file): 
        args = ["-f", "5", invalid_log]
        with pytest.raises(SystemExit): 
            util.main(args)
        captured = capsys.readouterr()
        expected_stdout, expected_stderr = expected_values_for_invalid_file
        assert captured.out == expected_stdout
        assert captured.err == expected_stderr

    def test_invalid_arg_with_stdin(self, capsys, monkeypatch, invalid_log, expected_values_reading_from_stdin, expected_values_for_invalid_file): 
        monkeypatch.setattr(sys, "stdin", io.StringIO(expected_values_reading_from_stdin[0]))
        args = ["-f", "5", invalid_log]
        with pytest.raises(SystemExit): 
            util.main(args)
        captured = capsys.readouterr()
        expected_stdout, expected_stderr = expected_values_for_invalid_file
        assert captured.out == expected_stdout
        assert captured.err == expected_stderr

    @staticmethod
    def mock_stdin_isatty(): 
        return True

    def test_no_arg_no_stdin(self, capsys, monkeypatch, expected_values_for_no_input): 
        monkeypatch.setattr(sys.stdin, "isatty", TestNegative.mock_stdin_isatty)
        args = []
        with pytest.raises(SystemExit): 
            util.main(args)
        captured = capsys.readouterr()
        expected_stdout, expected_stderr = expected_values_for_no_input
        assert captured.out == expected_stdout
        assert captured.err == expected_stderr



