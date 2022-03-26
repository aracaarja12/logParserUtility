#!/usr/bin/env python3

import argparse
import sys
import re
from pathlib import PurePath
from colorama import init, Back, Style

def has_stdin(): 
    return not sys.stdin.isatty()

def parse_cli_args(args): 
    '''
    Function to parse and error check command line arguments
        -f,--first and -l,--last consume a single integer above 0
        -t, -i, and -I are boolean switches
    Descriptions of each argument are given by the help parameter
    '''
    
    # Create the argument parser and define arguments
    parser = argparse.ArgumentParser(description="CLI application that helps you parse logs of various kinds")
    parser.add_argument("-f", "--first", metavar="NUM", type=int, help="print first NUM lines")
    parser.add_argument("-l", "--last", metavar="NUM", type=int, help="print last NUM lines")
    parser.add_argument("-t", "--timestamps", action="store_true", help="print lines that contain a timestamp in HH:MM:SS format")
    parser.add_argument("-i", "--ipv4", action="store_true", help="print lines that contain an IPv4 address, matching IPs are highlighted")
    parser.add_argument("-I", "--ipv6", action="store_true", help="print lines that contain an IPv6 address (standard notation), matching IPs are highlighted")
    parser.add_argument("file", metavar="FILE", type=argparse.FileType('r'), nargs="?", default=(None if not has_stdin() else sys.stdin), help="log file to be parsed")
    
    args = parser.parse_args(args)
    
    # Error checking not automatically handled by argparse
    if args.file is None: 
        parser.error("A file or standard input must be provided. Try -h for help.")
    int_args = (args.first, args.last)
    bool_args = (args.timestamps, args.ipv4, args.ipv6)
    if all(arg is None for arg in int_args) and all(not arg for arg in bool_args): 
        parser.error("At least one argument must be supplied as a filter. Try -h for help.")
    
    return args

def calculate_bounds(first, last, length): 
    '''
    Function to calculate the intersection of the --first and --last arguments
    Lines of the log that don't fall within this intersection will never be printed
    This function is intended to simplify computation
    '''
    
    # Assume the entire file will fall within the intersection
    boundaries = [0, length]
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
    
    # Edit the intersection... 
    if first is not None and last is None: # if only -f is given
        # boundaries = [0, f]
        boundaries[1] = first
    elif first is None and last is not None: # if only -l is given
        # boundaries = [length-l, length]
        boundaries[0] = length - last
    elif first is not None and last is not None: # if both -l and -f are given... 
        if first + last > length: # and there is an intersection
            # boundaries = [length - last, first]
            boundaries[0] = length - last 
            boundaries[1] = first
        else: # and there is no intersection
            boundaries = None
    
    return boundaries

def split_by_idx(line, indices): 
    '''
    Generator that splits a string by a list of indices
    '''
    
    front = 0
    back = indices[0]
    yield line[front:back]
    front = back
    for back in indices[1:]: 
        yield line[front:back]
        front = back
    yield line[front:]

def highlight_ip_addresses(line, matches): 
    '''
    Function to add highlighting to a string given a list of re.Match objects
    Returns the altered string
    '''
    
    # Split line into a list based on the given regex matches
    indices = []
    starts_with_ip = False
    for match in matches: 
        for i in match.span(): 
            if i == 0: 
                starts_with_ip = True
            elif i not in indices and i != len(line): 
                indices.append(i)
    segments = [*split_by_idx(line, indices)]
    
    # Color list elements that are IPs
    starting_position = 0 if starts_with_ip else 1
    for i in range(starting_position, len(segments), 2): 
        segments[i] = Back.GREEN + segments[i] + Style.RESET_ALL
    
    # Combine list into one string and return
    return "".join(segments)

def main(args): 
    '''
    Driver function
    '''
    
    # Parse command line arguments and consume input from the given file or stdin
    args = parse_cli_args(args)
    lines = args.file.readlines()
    args.file.close()
    
    # Find the intersection of the --first and --last arguments, return if there is no intersection
    boundaries = calculate_bounds(args.first, args.last, len(lines))
    if boundaries is None or boundaries in [[0,0], [len(lines),len(lines)]]: 
        return
    
    # Compile regex strings into regex pattern objects
    timestamp_re = re.compile(r"\b([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]\b")
    ipv4_re = re.compile(r"\b(([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\.){3}([01]?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\b")
    ipv6_re = re.compile(r"\b([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b")
    
    # True if lines in the intersection will contain IP addresses that must be highlighted
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
            line = highlight_ip_addresses(line, IP_match)
        if args.ipv6:
            IP_match = [*ipv6_re.finditer(line)]
            if not IP_match:
                continue
            line = highlight_ip_addresses(line, IP_match)
        
        print(line,end="")


if __name__ == "__main__": 
    main(sys.argv[1:])
