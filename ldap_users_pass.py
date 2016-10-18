#!/usr/bin/env python3
# coding: utf-8

"""Create a new list with all the users found in a list
who have an uncracked pass"""

import argparse


def parsing():
    """Parse the arguments for the scripts"""

    parser = argparse.ArgumentParser(prog='ldap_user_pass.py',
                                     usage='%(prog)s input output [OPTION]',
                                     description='Create a new dump with\
                                     user and pass')
    parser.add_argument('usernames',
                        help='Name of the file with the users')
    parser.add_argument('dump',
                        help='Name of the file from smart_hashdump')
    parser.add_argument('-o',
                        '--output',
                        default='resultats/users_pass.txt',
                        dest='output',
                        help='Name of the output file. (Default users_pass.txt)')

    return parser.parse_args()


def add_users(usernames, dump, output_file):
    """Add the users with uncracked passwords in a file

    Keyword arguments:
    usernames -- handler of the file with the john cracked passwords
    uncracked_pass -- handler of the dump from smart_hashdump
    output_file -- handler of the output file"""
    for line in usernames:
        dump.seek(0)
        for line2 in dump:
            full_line = line2.split(':')
            if len(full_line) == 5 and full_line[0] == line.strip("\n"):
                output_file.write(line2)
                break

def main():
    args = parsing()
    try:
        usernames = open(args.usernames, 'r')
    except IOError:
        print('Cannot open ', args.usernames)
    else:
        try:
            dump = open(args.dump, 'r')
        except IOError:
            print('Cannot open ', args.dump)
        else:
            try:
                output_file = open(args.output, 'w')
            except IOError:
                print('Cannot open ', args.output)
            else:
                add_users(usernames, dump, output_file)
                output_file.close()
                dump.close()
                usernames.close()

if __name__ == '__main__':
    main()
