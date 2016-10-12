#!/usr/bin/env python3
# coding: utf-8

"""Create password list from john the ripper output."""

import argparse


class johnDico:

    def parsing(self):
        """Parse the arguments for the scripts"""

        parser = argparse.ArgumentParser(prog='john_to_dico.py',
                                         usage='%(prog)s input output',
                                         description='LOL')
        parser.add_argument('input',
                            help='Name of the input file')
        parser.add_argument('output',
                            help='Name of the output file')

        self.args = parser.parse_args()

    def exists_in_file(self, word, output_file):
        """ Search if a word exists in the dictionnary.

        Keywords arguments:
        word -- the word to search
        output_file -- the handler of the file"""

        present = False
        output_file.seek(0)
        for line2 in output_file:
            if word == line2.strip("\n"):
                present = True
                break

        return present

    def write_word(self, input_file, output_file):
        """Add a word to a given file"""

        for line in input_file:
            password = line.strip("\n").split(':')[1]
            present = self.exists_in_file(password, output_file)
            if present is False:
                output_file.write(password + "\n")


def main():

    dictionnary = johnDico()
    dictionnary.parsing()
    try:
        input_file = open(dictionnary.args.input, 'r')
    except IOError:
        print('Cannot open ', dictionnary.args.input)
    else:
        try:
            output_file = open(dictionnary.args.output, 'a+')
        except IOError:
            print('Cannot open ', dictionnary.args.output)
        else:
            dictionnary.write_word(input_file, output_file)
            output_file.close()
        input_file.close()

if __name__ == '__main__':
    main()
