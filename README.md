# Log Parser Utility

This is a CLI application that helps you parse logs of various kinds. It prints the lines of a given log according to filters set by user-supplied command line arguments. The input log can be given as a command line argument or read from standard input. 

Presently, logParserUtility can detect timestamps of the form HH:MM:SS, IPv4 addresses, and IPv6 addresses in standard form that haven't been shortened with double colons. In the future, I hope to better optimize this tool and improve upon its IPv6 detection by adding to the relevant regex pattern. 

logParserUtility is also capable of filtering based on line number. The associated switches behave like the head and tail Linux commands but are not implemented using them. 

Colorama and pytest are required to highlight IP addresses and run the test suite, respectively. A requirements.txt file is available to help you install these into your environment.  

## Structure and contents

logParserUtility/
- util.py
- tests/
- - testLogs/
- - - various logs used by the test suite
- - \_\_init\_\_.py
- - conftest.py
- - test_first_and_last_options.py
- - test_input.py
- - test_timestamps_and_ips.py
- .gitignore
- LICENSE
- README.md
- \_\_init\_\_.py
- pytest.ini
- requirements.txt

| Item | Description |
| ------------- | ------------- |
| util.py | the application |
| tests/conftest.py | a pytest file presently being used to share fixtures between test modules |
| tests/test_first_and_last_options.py | tests pertaining to the --first and --last options |
| tests/test_input.py | tests pertaining to data input for tha application |
| tests/test_timestamps_and_ips.py | tests pertaining to the --timestamps, --ipv4, and --ipv6 options |
| LICENSE | an MIT license |
| pytest.ini | a pytest file defining markers for the test suite |
| requirements.txt | a text file outlining dependencies |

## How to install and run

This application has two dependencies, colorama and pytest. You can either install them directly or run the following command to make use of the supplied `requirements.txt` file. 

`pip install -r requirements.txt`

`util.py` can be executed without explicitly calling `python`. Usage follows: 

`./util.py [-h] [-f NUM] [-l NUM] [-t] [-i] [-I] [FILE]`

| Argument | Description |
| ------------- | ------------- |
| -h, --help | show this help message and exit |
| -f NUM, --first NUM | print the first NUM lines (a negative NUM value prints all but the last NUM lines) |
| -l NUM, --last NUM | print the last NUM lines (a negative NUM value is treated as though it were positive) |
| -t, --timestamps | print lines that contain a timestamp in HH:MM:SS format |
| -i, --ipv4 | print lines that contain an IPv4 address, matching IPs are highlighted |
| -I, --ipv6 | print lines that contain an IPv6 address (standard notation), matching IPs are highlighted |
| FILE | log file to be parsed |

All arguments are potentially optional, but there must be a data source and at least one argument for filtering. Error handling is included for these requirements. If valid data sources are given through both stdin and the FILE argument, logParserUtility defaults to using FILE. 

When a filtering argument is used, only lines from the data source that satisfy the given filter will be printed. If multiple filters are given, only lines that satisfy the intersection of these filters will be printed. There will be no output if all lines from the data source fail to satisfy each given filter. 

## Usage examples

| Example | Outcome |
| ------------- | ------------- |
| ./util.py -h | \<prints help\> |
| cat *log_name.log* \| ./util.py --first 10 | \<prints the first 10 lines of *log_name.log*\> |
| ./util.py -l 5 *log_name.log* | \<prints the last 5 lines of *log_name.log*\> |
| ./utils.py --timestamps *log_name.log* | \<prints any lines from *log_name.log* that contain a timestamp\> |
| ./util.py --ipv4 *log_name.log* | \<prints any lines from *log_name.log* that contain an IPv4 address\> |
| ./util.py --ipv6 *log_name.log* | \<prints any lines from *log_name.log* that contain an IPv6 address\> |
| ./util.py --ipv4 --last 50 *log_name.log* | \<prints any of the last 50 lines from *log_name.log* that contain an IPv4 address\> |

## Testing

Pytest is used for the test suite, which includes functional and unit tests. A built-in fixture called capsys is present in all of the functional tests, which define inputs to the application and assert its standard output and standard error. 

Standard input into the application is given with monkeypatch, another built-in fixture, where necessary. 

To run the test suite, navigate to the tests/ directory after installing logParserUtility's requirements and simply run: 

`pytest`

To run a specific module, give it as an argument to pytest: 

`pytest <module.py>`

Presently, all three modules each contain two classes: TestPositive and TestNegative. These contain the module's positive tests and negative tests, respectively. To run the negative tests from the test_input module, you can run: 

`pytest test_input.py::TestNegative`

In addition, I've marked each test as either a functional or unit test. This allows for the following: 

| Command | Outcome |
| ------------- | ------------- |
| pytest -m functional | \<runs all tests flagged as functional\> |
| pytest -m unit | \<runs all tests flagged as unit\> |

For more information on pytest, see https://docs.pytest.org/en/6.2.x/contents.html
