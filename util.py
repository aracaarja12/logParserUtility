#!C:\Users\Aaron\AppData\Local\Programs\Python\Python39\python.exe

import argparse
import sys

def main(args): 
	
	parser = argparse.ArgumentParser(description="CLI application that helps you parse logs of various kinds")
#	parser.add_argument("-h", "--help", )
	parser.add_argument("-f", "--first", metavar="NUM", type=int, nargs=1, help="Print first NUM lines")
	parser.add_argument("-l", "--last", metavar="NUM", type=int, nargs=1, help="Print last NUM lines")
	parser.add_argument("-t", "--timestamp", action="store_true", help="Print lines that contain a timestamp in HH:MM:SS format")
	parser.add_argument("-i", "--ipv4", action="store_true", help="Print lines that contain an IPv4 address, matching IPs are highlighted")
	parser.add_argument("-I", "--ipv6", action="store_true", help="Print lines that contain an IPv6 address (standard notation), matching IPs are highlighted")
	parser.add_argument("file", metavar="FILE", type=str, nargs="?", help="Log file to be parsed")
	
	args = parser.parse_args(args)
	
	print(args)
	
if __name__ == "__main__": 
	main(sys.argv[1:])
