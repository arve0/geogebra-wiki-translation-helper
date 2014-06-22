#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
File: report.py
Author: Arve Seljebu
Email: arve.seljebu@gmail.com
Github: arve0
Description: Generates a report on defferences between english and given wiki.
"""

import sys
from wikipages import WikiPages
from commands import Commands
import config

if sys.version_info[0] != 2:
    print 'This program is written for python2, as pywikibot uses python2.'
    sys.exit()

pages_dict = {}
commands_dict = {}


def initialize_pages():
    """ Set up pages_dict """
    for language in config.LANGUAGES:
        pages_dict[language.code] = WikiPages(language.name, language.code)


def get_and_store_wikipages():
    """ Get list of all pages and store it to json """

    initialize_pages()
    for language in config.LANGUAGES:
        pages_dict[language.code].load_from_wiki()
        pages_dict[language.code].save_to_json()


def get_wiki_pages_from_disk():
    """ Get wiki pages from json """

    initialize_pages()
    for language in config.LANGUAGES:
        pages_dict[language.code].load_from_json()


def initialize_commands():
    """ Set up commands_dict """
    for language in config.LANGUAGES:
        commands_dict[language.code] = Commands(language.name, language.code)


def get_and_store_commands():
    """ Get commands from svn and store to disk """

    initialize_commands()
    for language in config.LANGUAGES:
        commands_dict[language.code].load_from_svn()
        commands_dict[language.code].save_to_json()


def get_commands_from_disk():
    """ Get commands from json files """

    initialize_commands()
    for language in config.LANGUAGES:
        commands_dict[language.code].load_from_json()


def analyze_missing_pages():
    """ Find missing pages (not translated from english) """
    header = 'Loading from disk'
    print header
    print '='*len(header)
    get_wiki_pages_from_disk()
    get_commands_from_disk()
    print ''

    header = 'Number of pages'
    print header
    print '='*len(header)
    for language in config.LANGUAGES:
        pages_dict[language.code].print_status()
        commands_dict[language.code].print_status()
        i = 0
        cmd = []
        for page in pages_dict[language.code].pages:
            for command in commands_dict[language.code].commands:
                if command in page['title']:
                    i += 1
                    cmd.append(page['title'])
        print i
    print ''


def main(argv):
    """ process args """
    if 'get-wiki' in argv:
        get_and_store_wikipages()
    elif 'get-commands' in argv:
        get_and_store_commands()
    elif 'analyze' in argv:
        analyze_missing_pages()
    else:
        print 'Usage:'
        print argv[0] + ' command\n'
        print 'List of commands:'
        print 'analyze \t- reads data from json and analyzes it'
        print 'get-commands \t- gets a list of all command commands from SVN and stores it to a json file'
        print 'get-wiki \t- gets a list of all pages from wiki and stores it to a json file'


if __name__ == '__main__':
    main(sys.argv)
