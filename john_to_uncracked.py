#!/usr/bin/env python3
# coding: utf-8

"""Add cracked passwords from john.pot to a dump
from the metasploit module smart_hashdump"""

import argparse


def parsing():
    """Parse the arguments for the scripts"""

    parser = argparse.ArgumentParser(prog='john_to_uncracked.py',
                                     usage='%(prog)s input output',
                                     description='Add cracked passwords\
                                     to smart_hashdump dump')
    parser.add_argument('cracked',
                        help='Name of the file with cracked passwords')
    parser.add_argument('uncracked',
                        help='Name of the file from smart_hashdump')
    parser.add_argument('-o',
                        '--output',
                        default='new_hash.txt',
                        dest='output',
                        help='Name of the output file. Combinastion of\
                        the cracked passwords and the smart_hashdump file')

    return parser.parse_args()


def add_pass(cracked_pass, uncracked_pass, output_file):
    """Add the cracked passwords to the dump from smart_hashdump.

    Keyword arguments:
    cracked_pass -- handler of the file with the john cracked passwords
    uncracked_pass -- handler of the dump from smart_hashdump
    output_file -- handler of the output file (default new_hash.txt)"""
    for line in uncracked_pass:
        if len(line.split(':')) == 5:
            output_file.write(line)
        else:
            present = False
            hashpass = line.strip("\n").split(':')[3]
            cracked_pass.seek(0)
            for line2 in cracked_pass:
                foo = line2.replace("$NT$", "", 1).strip("\n").split(':')[0]
                if hashpass == foo:
                    password = line2.strip("\n").split(':')[1]
                    output_file.write(line.strip("\n") + ":" + password + "\n")
                    present = True
                    break
            if present is False:
                output_file.write(line)


def main():
    args = parsing()
    try:
        cracked_pass = open(args.cracked, 'r')
    except IOError:
        print('Cannot open ', args.cracked)
    else:
        try:
            uncracked_pass = open(args.uncracked, 'r')
        except IOError:
            print('Cannot open ', args.uncracked)
        else:
            try:
                output_file = open(args.output, 'w')
            except IOError:
                print('Cannot open ', args.output)
            else:
                add_pass(cracked_pass, uncracked_pass, output_file)
                output_file.close()
                uncracked_pass.close()
                cracked_pass.close()

if __name__ == '__main__':
    main()
