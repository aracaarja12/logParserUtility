#!C:\Users\Aaron\AppData\Local\Programs\Python\Python39\python.exe

import argparse
import sys

def parse_cli_args(args): 

	parser = argparse.ArgumentParser(description="CLI application that helps you parse logs of various kinds")
	parser.add_argument("-f", "--first", metavar="NUM", type=int, nargs=1, help="Print first NUM lines")
	parser.add_argument("-l", "--last", metavar="NUM", type=int, nargs=1, help="Print last NUM lines")
	parser.add_argument("-t", "--timestamp", action="store_true", help="Print lines that contain a timestamp in HH:MM:SS format")
	parser.add_argument("-i", "--ipv4", action="store_true", help="Print lines that contain an IPv4 address, matching IPs are highlighted")
	parser.add_argument("-I", "--ipv6", action="store_true", help="Print lines that contain an IPv6 address (standard notation), matching IPs are highlighted")
	parser.add_argument("file", metavar="FILE", type=argparse.FileType('r'), nargs="?", default=(None if sys.stdin.isatty() else sys.stdin), help="Log file to be parsed")
	
	args = parser.parse_args(args)
	if args.file == None: 
		parser.error("A file or standard input must be provided")
	return args

def calculateBounds(first, last, length): 
	boundaries = [0,length]
	print(first)
	print(last)
	print(length)
	if first != None: 
		first = length if first > length else first
	if last != None:
		last = length if last > length else last
		
	# constant operation to find the bounds based on -f and -t if they exist
	# CASE where neither l or f
	if first == None and last == None: 
		# boundaries = [0,len(lines)]
		pass
	# CASE where only f
	elif last == None:
		# boundaries = [0,f]
		boundaries[1] = first
	# CASE where only l
	elif first == None:
		# boundaries = [len(lines)-l,len(lines)]
		boundaries[0] = length - last
	# CASE where both l and f
	else: 
		# if (l + f) > len(lines), i.e. there is an intersection
		if first + last > length:
			# boundaries = [length - last, first]
			boundaries[0] = length - last 
			boundaries[1] = first
		# else there is no intersection
		else: 
			boundaries = None
	
	return boundaries
	
def hasTimestamp(line):
	pass
	
def hasIPv4(line):
	pass
	
def hasIPv6(line):
	pass
	
def main(args): 
	
	args = parse_cli_args(args)
	print(args)
	
	lines = args.file.readlines()
	print(lines)
	args.file.close()
	
	first = args.first[0] if args.first != None else None
	last = args.last[0] if args.last != None else None
	boundaries = calculateBounds(first,last,len(lines))
	print("Boundaries are:", boundaries)
	
	for line in lines[boundaries[0]:boundaries[1]]: 
		# t, ipv4, ipv6
		if args.timestamp:
			if not hasTimestamp(line):
				continue
		if args.ipv4:
			if not hasIPv4(line):
				continue
		if args.ipv6:
			if not hasIPv6(line):
				continue
		print(line)
		#if inIntersection(line): 
		#	print(line)
	
	# linear operation to iterate through the bounds and verify each row
		# for each line in the bounds
			# if args.timestamp == True
				# if line doesn't have timestamp
					# continue
			# if args.ipv4 == True
				# if line doesn't have ipv4
					# continue
			# if args.ipv6 == True
				# if line doesn't have ipv6
					# continue
			# print line
	
	# iterate through every line and populate multiple sets based on conditions
	# find intersection
	# iterate through the intersection to print
	
	
if __name__ == "__main__": 
	main(sys.argv[1:])
