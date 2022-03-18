#!C:\Users\Aaron\AppData\Local\Programs\Python\Python39\python.exe

import argparse
import sys
import re

def parse_cli_args(args): 
	'''
	Function to parse and error check command line arguments
		-f,--first and -l,--last consume a single integer above 0
		-t, -i, and -I are boolean switches
	Descriptions of each argument are given by the help parameter
	More verbose descriptions can be found in the README
	'''
	
	# Create the argument parser and define arguments
	parser = argparse.ArgumentParser(description="CLI application that helps you parse logs of various kinds")
	parser.add_argument("-f", "--first", metavar="NUM", type=int, help="Print first NUM lines")
	parser.add_argument("-l", "--last", metavar="NUM", type=int, help="Print last NUM lines")
	parser.add_argument("-t", "--timestamp", action="store_true", help="Print lines that contain a timestamp in HH:MM:SS format")
	parser.add_argument("-i", "--ipv4", action="store_true", help="Print lines that contain an IPv4 address, matching IPs are highlighted")
	parser.add_argument("-I", "--ipv6", action="store_true", help="Print lines that contain an IPv6 address (standard notation), matching IPs are highlighted")
	parser.add_argument("file", metavar="FILE", type=argparse.FileType('r'), nargs="?", default=(None if sys.stdin.isatty() else sys.stdin), help="Log file to be parsed")
	
	args = parser.parse_args(args)
	
	# Error checking not automatically handled by argparse
	if args.file is None: 
		parser.error("A file or standard input must be provided")
	if args.first is not None: 
		if args.first < 1: 
			parser.error("Numbers supplied to --first must be integers greater than 0")
	if args.last is not None: 
		if args.last < 1: 
			parser.error("Numbers supplied to --last must be integers greater than 0")
	
	return args

def calculateBounds(first, last, length): 
	'''
	Function to calculate the intersection of the --first and --last arguments
	Lines of the log that don't fall within this intersection will never be printed
	This function is intended to simplify computation
	'''
	
	# Assume the entire file will fall within the intersection
	# Note: this function silently corrects values of --first and --last that exceed the length of the log
	boundaries = [0,length]
	if first is not None: 
		first = length if first > length else first
	if last is not None:
		last = length if last > length else last
	
	# Find the intersection... 
	if first is None and last is None: # where neither -l or -f is given
		# boundaries = [0,length]
		pass
	elif last is None: # where only -f is given
		# boundaries = [0,f]
		boundaries[1] = first
	elif first is None: # where only -l is given
		# boundaries = [length-l,length]
		boundaries[0] = length - last
	else: # where both -l and -f are given... 
		if first + last > length: # and there is an intersection
			# boundaries = [length - last, first]
			boundaries[0] = length - last 
			boundaries[1] = first
		else: # and there is no intersection
			boundaries = None
	
	return boundaries

def displaymatch(match): 
	if match is None: 
		print("None")
	print("<Match %r, groups=%r>" % (match.group(),match.groups()))

def main(args): 
	'''
	Driver function
	'''
	
	# Parse command line arguments and consume input from the given file or stdin
	args = parse_cli_args(args)
	lines = args.file.readlines()
	args.file.close()
	
	# Find the intersection of the --first and --last arguments
	boundaries = calculateBounds(args.first,args.last,len(lines))
	
	# Compile regex strings into regex objects to speed up runtime
	timestamp_re = re.compile(r"([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]")
	ipv4_re = re.compile(r"(([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\.){3}([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])")
	ipv6_re = re.compile(r"([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}")
	
	# Print each line in the intersection of the given arguments
	for line in lines[boundaries[0]:boundaries[1]]: 
		if args.timestamp:
			if not timestamp_re.search(line):
				continue
		if args.ipv4:
			if not ipv4_re.search(line):
				continue
		if args.ipv6:
			if not ipv6_re.search(line):
				continue
		print(line)


if __name__ == "__main__": 
	main(sys.argv[1:])
