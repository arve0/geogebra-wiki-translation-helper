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


def update_cache(language, namespace):
    """Update cache of given language and namespace."""
    suffix = '-' + language + '-' + namespace

    msg = u'Updating cache for {0}, namespace {1}'\
            .format(Language(language), namespace)
    print msg
    print '='*len(msg)

    pages = Cache(Pages(namespace=namespace, language=language).get,
                  'pages' + suffix, force=True)
    commands = Cache(Commands(language, pages=pages.data).get,
                     'commands-' + language, force=True)


def find_missing(language, namespace):
    """Find missing pages (not translated from english or not added to wiki)."""
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
    msg = u'Missing command pages in {0}, namespace {1}'\
            .format(Language(language), namespace)
    print msg
    print '='*len(msg)

    for command in commands.data.itervalues():
        if 'wikiid' not in command.keys():
            print u'Wikipage missing for command {0}'\
                    .format(command['translation'])


def find_updated(language, namespace):
    """Find command pages which is updated in English wiki."""
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

    # Updated pages
    print ''
    msg = u'Updated command pages in {0}, namespace {1}'\
            .format(Language(language), namespace)
    print msg
    print '='*len(msg)

    for (command_name, command) in commands.data.iteritems():
        if 'wikiid' not in command.keys():
            # command does not exist in wiki
            continue

        page = [p for p in pages.data if p['id'] == command['wikiid']]
        en_command = en_commands.data[command_name]
        en_page = [p for p in en_pages.data if p['id'] == en_command['wikiid']]

        # make sure we get only one match
        assert len(page) == 1 and len(en_page) == 1
        page = page[0]
        en_page = en_page[0]

        # short names
        title = page['title']
        time = page['editTime']
        en_title = en_page['title']
        en_time = en_page['editTime']
        if time < en_time:
            # put time 50 chars to right
            print u'{0} updated\r\x1b[50C{1}'.format(title, time)
            print u'{0} updated\r\x1b[50C{1}'.format(en_title, en_time)
            print ''


def print_usage():
    """
    Print usage of this script.
    """

    usage = '''
    Usage
    =====
    {0} command language [namespace]

    Commands
    ========
    cache: \tUpdate cache of given language and namespace.

    missing: \tFind missing command wikipages.
    
    updated: \tFind wikipages with newer/updated English version.


    Default values
    ==============
    namespace: 'Manual'
'''.format(sys.argv[0])

    print usage


def main():
    """ process args """
    length = len(sys.argv)
    if length == 4:
        language = sys.argv[2].lower()
        namespace = sys.argv[3].capitalize()
    elif length == 3:
        language = sys.argv[2].lower()
        namespace = 'Manual'
    else:
        print_usage()
        sys.exit()

    cmd = sys.argv[1]
    if cmd == 'cache':
        update_cache(language, namespace)
    elif cmd == 'missing':
        find_missing(language, namespace)
    elif cmd == 'updated':
        find_updated(language, namespace)


    #try:
        #analyze(argv[1], argv[2])
    #except IndexError:
        #try:
            #analyze(argv[1])
        #except IndexError:
            #print_usage()
        #except NameError as error:
            #print error
            #print_usage()


if __name__ == '__main__':
    main()
