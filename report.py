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
from sources import Pages
from sources import Commands
from cache import Cache
from language import Language


if sys.version_info[0] != 2:
    print 'This program is written for python2, as pywikibot uses python2.'
    sys.exit()


def analyze(language, namespace='Manual'):
    """ Find missing pages (not translated from english) """
    namespace = namespace.lower().capitalize()
    language = language.lower()
    suffix = '-' + language + '-' + namespace

    msg = 'Getting pages and commands to work with'
    print msg
    print '='*len(msg)

    en_pages = Cache(Pages(namespace=namespace).get, 'pages-en-' + namespace)
    pages = Cache(Pages(namespace=namespace, language=language).get,
                  'pages' + suffix)

    en_commands = Cache(Commands(pages=en_pages.data).get, 'commands-en')
    commands = Cache(Commands(language, pages=pages.data).get,
                     'commands-' + language)

    # Missing pages
    print ''
    msg = u'Missing pages in {0}, namespace {1}'\
            .format(Language(language), namespace)
    print msg
    print '='*len(msg)

    for command in commands.data.itervalues():
        if 'wikiid' not in command.keys():
            print u'Wikipage missing for command {0}'\
                    .format(command['translation'])


def print_usage():
    """
    Print usage of this script.
    """

    usage = '''
    Usage:
    {0} language [namespace]

    Compares given language to English wiki.

    Default values:
    namespace: 'Manual'
'''.format(sys.argv[0])

    print usage


def main(argv):
    """ process args """
    try:
        analyze(argv[1], argv[2])
    except IndexError:
        try:
            analyze(argv[1])
        except IndexError:
            print_usage()
        except NameError as error:
            print error
            print_usage()


if __name__ == '__main__':
    main(sys.argv)
