# Log Parsing Utility

This is a CLI application that helps you parse logs of various kinds. It prints the lines of a given log according to filters set by command line arguments. With the exception of colorama for highlighting IP addresses, the implementation for this uses only Python's standard library. 

In the future, I hope to better optimize this tool and improve upon its IPv6 detection. Presently, logParserUtility is only capable of detecting IPv6 addresses in standard form that haven't been shortened with double colons, and I'd like to improve upon this. 

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

util.py -- the application

tests.py -- the test suite for the application

## How to install and run

This application has one dependency, colorama. You can either install it directly or run the following command to make use of the supplied `requirements.txt` file. 

`pip install -r requirements.txt`

A shebang is included in `util.py` to allow for execution without explicitly calling `python`. Usage follows: 

`./util.py \[-h\] \[-f NUM\] \[-l NUM\] \[-t\] \[-i\] \[-I\] \[FILE\]`

| Argument | Description |
| ------------- | ------------- |
| -h, --help | show this help message and exit |
| -f NUM, --first NUM | print first NUM lines |
| -l NUM, --last NUM | print last NUM lines |
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

