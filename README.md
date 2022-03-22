# Log Parsing Utility

This is a CLI application that helps you parse logs of various kinds. It prints the lines of a given log according to filters set by user-supplied command line arguments. The input log can be given as a command line argument or read from standard input. 

With the exception of colorama for highlighting IP addresses, the implementation for this uses only Python's standard library. 

Presently, logParserUtility detects IPv6 addresses in standard form that haven't been shortened with double colons. In the future, I hope to better optimize this tool and improve upon its IPv6 detection by adding to the relevant regex pattern. 

## Structure and contents

logParserUtility/
- .gitignore
- LICENSE
- README.md
- requirements.txt
- testLogs/
- - various logs for testing
- tests.py
- util.py

| Item | Description |
| ------------- | ------------- |
| LICENSE | an MIT license |
| requirements.txt | text file outlining dependencies |
| testLogs | directory for logs used by tests in tests.py |
| tests.py | the test suite for the application |
| util.py | the application |

## How to install and run

This application has one dependency, colorama. You can either install it directly or run the following command to make use of the supplied `requirements.txt` file. 

`pip install -r requirements.txt`

A shebang is included in `util.py` to allow for execution without explicitly calling `python`. Usage follows: 

`./util.py \[-h\] \[-f NUM\] \[-l NUM\] \[-t\] \[-i\] \[-I\] \[FILE\]`

| Argument | Description |
| ------------- | ------------- |
| -h, --help | show this help message and exit |
| -f NUM, --first NUM | print the first NUM lines (a negative NUM value prints from the back) |
| -l NUM, --last NUM | print the last NUM lines (a negative NUM value is treated as though it were positive) |
| -t, --timestamps | print lines that contain a timestamp in HH:MM:SS format |
| -i, --ipv4 | print lines that contain an IPv4 address, matching IPs are highlighted |
| -I, --ipv6 | print lines that contain an IPv6 address (standard notation), matching IPs are highlighted |
| FILE | log file to be parsed |

All arguments are optional, but the result is the intersection of the arguments' results, so no output will be generated if no arguments are used. If FILE is omitted, standard input is used instead. 

## Usage examples

| Example | Outcome |
| ------------- | ------------- |
| ./util.py -h | \<prints help\> |
| cat test_0.log \| ./util.py --first 10 | \<prints the first 10 lines of test_0.log\> |
| ./util.py -l 5 test_1.log | \<prints the last 5 lines of test_1.log\> |
| ./utils.py --timestamps test_2.log | \<prints any lines from test_2.log that contain a timestamp\> |
| ./util.py --ipv4 test_3.log | \<prints any lines from test_3.log that contain an IPv4 address\> |
| ./util.py --ipv6 test_4.log | \<prints any lines from test_4.log that contain an IPv6 address\> |
| ./util.py --ipv4 --last 50 test_5.log | \<prints any of the last 50 lines from test_5.log that contain an IPv4 address\> |

## Testing

