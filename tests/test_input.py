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

@pytest.fixture(scope="module")
def expected_values_reading_from_stdin(): 
    return (
        (
		    "This is line 1 Reading from stdin\n192.168.255.0 This is line 2 "
			"1762:0:0:0:0:B03:1:AF18\nThis is line 3 12:24:59\nThis is line 4 "
			"256.256.256.0\nThis is line 5 172.16.254.1"
		), 
        ""
    )

def mock_stdin_isatty(): 
    return True

class TestPositive: 

    @pytest.fixture(scope="class")
    def log_from_arg(self): 
        return str(PurePath("testLogs/test_input_from_arg.log"))

    @pytest.fixture(scope="class")
    def expected_values_reading_from_arg(self): 
        return (
            (
			    "This is line 1 Reading from argument\n192.168.255.0 This is "
				"line 2 1762:0:0:0:0:B03:1:AF18\nThis is line 3 12:24:59\n"
				"This is line 4 256.256.256.0\nThis is line 5 172.16.254.1"
			), 
            ""
        )

    @pytest.mark.functional
    def test_valid_arg_no_pipe(
            self, capsys, monkeypatch, log_from_arg, 
            expected_values_reading_from_arg): 
        monkeypatch.setattr(sys.stdin, "isatty", mock_stdin_isatty)
        args = ["-f", "5", log_from_arg]
        util.main(args)
        captured = capsys.readouterr()
        expected_stdout, expected_stderr = expected_values_reading_from_arg
        assert captured.out == expected_stdout
        assert captured.err == expected_stderr

    @pytest.mark.functional
    def test_valid_arg_with_pipe(
            self, capsys, monkeypatch, log_from_arg, 
            expected_values_reading_from_stdin, 
            expected_values_reading_from_arg): 
        monkeypatch.setattr(
            sys, "stdin", io.StringIO(expected_values_reading_from_stdin[0]))
        args = ["-f", "5", log_from_arg]
        util.main(args)
        captured = capsys.readouterr()
        expected_stdout, expected_stderr = expected_values_reading_from_arg
        assert captured.out == expected_stdout
        assert captured.err == expected_stderr

    @pytest.mark.functional
    def test_no_arg_with_pipe(
            self, capsys, monkeypatch, expected_values_reading_from_stdin): 
        monkeypatch.setattr(
            sys, "stdin", io.StringIO(expected_values_reading_from_stdin[0]))
        args = ["-f", "5"]
        util.main(args)
        captured = capsys.readouterr()
        expected_stdout, expected_stderr = expected_values_reading_from_stdin
        assert captured.out == expected_stdout
        assert captured.err == expected_stderr

class TestNegative: 

    @pytest.fixture(scope="class")
    def script_name(self): 
        return PurePath(sys.argv[0]).parts[-1]

    @pytest.fixture(scope="class")
    def invalid_log(self): 
        return "invalid.log"

    @pytest.fixture(scope="class")
    def expected_values_for_invalid_file(self, script_name, invalid_log): 
        return (
            "",
            (
                f"usage: {script_name} [-h] [-f NUM] [-l NUM] [-t] [-i] [-I] "
				f"[FILE]\n{script_name}: error: argument FILE: can't open '"
				f"{invalid_log}': [Errno 2] No such file or directory: '"
				f"{invalid_log}'\n"
			)
        )

    @pytest.fixture(scope="class")
    def expected_values_for_no_input(self, script_name): 
        return (
            "", 
            (
                f"usage: {script_name} [-h] [-f NUM] [-l NUM] [-t] [-i] [-I] "
				f"[FILE]\n{script_name}: error: A file or standard input must "
				"be provided. Try -h for help.\n"
			)
        )
    
    @pytest.mark.functional
    def test_invalid_arg_no_pipe(
            self, capsys, monkeypatch, invalid_log, 
            expected_values_for_invalid_file): 
        monkeypatch.setattr(sys.stdin, "isatty", mock_stdin_isatty)
        args = ["-f", "5", invalid_log]
        with pytest.raises(SystemExit): 
            util.main(args)
        captured = capsys.readouterr()
        expected_stdout, expected_stderr = expected_values_for_invalid_file
        assert captured.out == expected_stdout
        assert captured.err == expected_stderr

    @pytest.mark.functional
    def test_invalid_arg_with_pipe(
            self, capsys, monkeypatch, invalid_log, 
            expected_values_reading_from_stdin, 
            expected_values_for_invalid_file): 
        monkeypatch.setattr(
            sys, "stdin", io.StringIO(expected_values_reading_from_stdin[0]))
        args = ["-f", "5", invalid_log]
        with pytest.raises(SystemExit): 
            util.main(args)
        captured = capsys.readouterr()
        expected_stdout, expected_stderr = expected_values_for_invalid_file
        assert captured.out == expected_stdout
        assert captured.err == expected_stderr

    @pytest.mark.functional
    def test_no_arg_no_pipe(
            self, capsys, monkeypatch, expected_values_for_no_input): 
        monkeypatch.setattr(sys.stdin, "isatty", mock_stdin_isatty)
        args = []
        with pytest.raises(SystemExit): 
            util.main(args)
        captured = capsys.readouterr()
        expected_stdout, expected_stderr = expected_values_for_no_input
        assert captured.out == expected_stdout
        assert captured.err == expected_stderr
