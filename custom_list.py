#!/usr/bin/env python3
# coding: utf-8
"""This script create a custom list of passwords."""


import argparse
import datetime


TODAY = datetime.date.today()


def parsing():
    """Parse the arguments for the script"""
    parser = argparse.ArgumentParser(prog='custom_list.py',
                                     usage='%(prog)s words [OPTIONS]',
                                     description='Create custom passwords list.\
                                     Capitalize some letters:\
                                     dog => Dog, DOg, DOG,dOg etc.\
                                     Add number from 0 to 99 \
                                     and from 1950 to 2016\
                                     at the end of the passwords')
    parser.add_argument('words',
                        nargs='+',
                        action='append',
                        help='List of known words, separated by space.')
    parser.add_argument('-o',
                        '--output',
                        dest='output',
                        default='wordlist.txt',
                        help='Name of the output file.\
                        (Default: wordlist.txt)')
    parser.add_argument('-p',
                        '--prefix',
                        dest='prefix',
                        default='',
                        help='Prefix every password generated with one word')
    parser.add_argument('-s',
                        '--suffix',
                        dest='suffix',
                        nargs='+',
                        action='append',
                        help='Add multiple suffixes to password')
    return parser.parse_args()


def password_generator(word, wordlist, prefix='', suffix=None):
    """Generate and write a list of passwords in a file

    Keyword arguments:
    word -- The base word from wich the passwords are generated
    wordlist -- handler of the file
    prefix -- Word which will be written before all the passwords (default '')
    suffix -- Adde a suffix to the base word (defaut None)
    """
    nb_password = 0
    for x in range(0, 2**len(word)):
        new_password = prefix
        for i in range(0, len(word)):
            if 2**i & x == 0:
                new_password += word[i].upper()
            else:
                new_password += word[i]
        wordlist.write(new_password + "\n")
        nb_password += 1
        if suffix is not None:
            for suf in suffix[0]:
                wordlist.write(new_password + suf + "\n")
                nb_password += 1
        for i in range(0, 100):
            wordlist.write(new_password + str(i) + "\n")
            nb_password += 1
        for i in range(2005, (TODAY.year + 1)):
            wordlist.write(new_password + str(i) + "\n")
            nb_password += 1

    return nb_password


def main():
    nb_passwords = 0
    args = parsing()
    try:
        wordlist = open(args.output, 'w')
    except IOError:
        print('Cannot open', args.output)
    else:
        for word in args.words[0]:
            nb_passwords += password_generator(word,
                                               wordlist,
                                               args.prefix,
                                               args.suffix)

        wordlist.close()
        print("{} passwords created." .format(nb_passwords))

main()
