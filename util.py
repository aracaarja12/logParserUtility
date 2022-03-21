#!C:\Users\Aaron\AppData\Local\Programs\Python\Python39\python.exe

import argparse
import sys
import re
from colorama import init, Back, Style
from operator import itemgetter

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
	parser.add_argument("-t", "--timestamps", action="store_true", help="Print lines that contain a timestamp in HH:MM:SS format")
	parser.add_argument("-i", "--ipv4", action="store_true", help="Print lines that contain an IPv4 address, matching IPs are highlighted")
	parser.add_argument("-I", "--ipv6", action="store_true", help="Print lines that contain an IPv6 address (standard notation), matching IPs are highlighted")
	parser.add_argument("file", metavar="FILE", type=argparse.FileType('r'), nargs="?", default=(None if sys.stdin.isatty() else sys.stdin), help="Log file to be parsed")
	
	args = parser.parse_args(args)
	
	# Error checking not automatically handled by argparse
	if args.file is None: 
		parser.error("A file or standard input must be provided")
	
	return args

def calculateBounds(first, last, length): 
	'''
	Function to calculate the intersection of the --first and --last arguments
	Lines of the log that don't fall within this intersection will never be printed
	This function is intended to simplify computation
	'''
	
	# Assume the entire file will fall within the intersection
	boundaries = [0,length]
	if first is not None: 
		# Correct values of --first to support negative indexing, prevent errors, and mimic the head utility
		if first < 0-length: 
			first = 0
		elif first < 0: 
			first = length + first
		elif first > length: 
			first = length
	if last is not None:
		# Correct values of --last to prevent errors and mimic the tail utility
		if last < 0-length or last > length: 
			last = length
		elif last < 0: 
			last = abs(last)
	
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

'''
def displaymatch(match): 
	if match is None: 
		print("None")
	print("<Match %r, groups=%r>" % (match.group(),match.groups()))
'''

def splitByIdx(line, indices): 
	front = 0
	back = indices[0]
	yield line[front:back]
	front = back
	for back in indices[1:]: 
		yield line[front:back]
		front = back
	yield line[front:]

def highlightIPs(line, matches): 
	# split line into a list
	indices = []
	startsWithIP = False
	for match in matches: 
		for i in match.span(): 
			if i == 0: 
				startsWithIP = True
			elif i not in indices and i != len(line): 
				indices.append(i)
	segments = [*splitByIdx(line,indices)]
	
	# color list elements that are IPs
	startingPosition = 0 if startsWithIP else 1
	for i in range(startingPosition,len(segments),2): 
		segments[i] = Back.GREEN + segments[i] + Style.RESET_ALL
	
	# combine list into one string and return
	return "".join(segments)

def testhighlight(): 
	s = "up what's up doc up doc up up up"
	iter = re.compile("up").finditer(s)
	print(highlightIPs(s,iter))

def main(args): 
	'''
	Driver function
	'''
	
	# Parse command line arguments and consume input from the given file or stdin
	args = parse_cli_args(args)
	lines = args.file.readlines()
	args.file.close()
	
	# Find the intersection of the --first and --last arguments, return if there is no intersection
	boundaries = calculateBounds(args.first,args.last,len(lines))
	if boundaries is None: 
		return
	
	# Compile regex strings into regex pattern objects
	timestamp_re = re.compile(r"([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]")
	ipv4_re = re.compile(r"(([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\.){3}([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])")
	ipv6_re = re.compile(r"([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}")
	
	# True if lines in the intersection will contain IP addresses that must be highlighted
	#IPs_included = args.ipv4 or args.ipv6
	if args.ipv4 or args.ipv6: 
		init()
	IP_match = None
	
	# Print each line in the intersection of the given arguments
	for line in lines[boundaries[0]:boundaries[1]]: 
		if args.timestamps:
			if not timestamp_re.search(line):
				continue
		if args.ipv4:
			IP_match = [*ipv4_re.finditer(line)]
			if not IP_match:
				continue
			line = highlightIPs(line, IP_match)
		if args.ipv6:
			#IP_match = ipv6_re.search(line)
			IP_match = [*ipv6_re.finditer(line)]
			if not IP_match:
				continue
			line = highlightIPs(line, IP_match)
		
		#if IP_match: 
			#line = line[:IP_match.span()[0]] + Back.GREEN + line[IP_match.span()[0]:IP_match.span()[1]] + Style.RESET_ALL + line[IP_match.span()[1]:]
		
		print(line,end="")


if __name__ == "__main__": 
	main(sys.argv[1:])
	#testhighlight()
