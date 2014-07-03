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
import pywikibot

# utf8 hack
# http://stackoverflow.com/questions/492483/setting-the-correct-encoding-when-piping-stdout-in-python
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

if sys.version_info[0] != 2:
    print u'This program is written for python2, as pywikibot uses python2.'
    sys.exit()


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

    size: \tFind wikipages with large size difference to English version.

    updated: \tFind wikipages with newer/updated English version.

    wiki: \tRun all reports and upload the report to wiki.

    Default values
    ==============
    namespace: 'Manual' - Should be in english. Eg: Main, Manual.
                          List here http://wiki.geogebra.org/en/Special:Categories
'''.format(sys.argv[0])

    print usage


def update_cache(language, namespace):
    """Update cache of given language and namespace."""
    suffix = '-' + language + '-' + namespace

    msg = u'Updating cache for {0}, namespace {1}'\
            .format(Language(language), namespace)
    print msg
    print u'='*len(msg)

    pages = Cache(Pages(namespace=namespace, language=language).get,
                  'pages' + suffix, force=True)
    commands = Cache(Commands(language, pages=pages.data).get,
                     'commands-' + language, force=True)

    # deletion invokes saving of cache
    del pages
    del commands


def find_missing(language, namespace, console_output=False):
    """Find missing pages (not translated from english or not added to wiki)."""
    suffix = '-' + language + '-' + namespace

    print u'Getting pages and commands from cache'

    pages = Cache(Pages(namespace=namespace, language=language).get,
                  'pages' + suffix)

    commands = Cache(Commands(language, pages=pages.data).get,
                     'commands-' + language)

    # Missing pages
    msg = u'== Missing command pages ==\n'
    if console_output:
        print msg

    msg += u'{| class="wikitable"\n'
    msg += u'|- <!-- header -->\n'
    msg += u'! Missing !! English page\n'

    row = 1
    cmd_string = u' ' + commands.data['Command']['translation']
    for (command_key, command) in commands.data.iteritems():
        if 'wikiid' not in command.keys():
            if console_output:
                print (u'Wikipage missing for command {0}'
                       .format(command['translation']))
            title = command['translation'] + cmd_string
            link = namespace + u':' + title
            en_title = command_key + u' Command'
            en_link = namespace + u':' + en_title
            msg += u'|- <-- row {0} -->\n'.format(row)
            row += 1
            msg += (u'| [[{0}|{1}]] || [[:en:{2}|{3}]]\n'
                    .format(link, title, en_link, en_title))

    msg += u'|}\n'

    return msg


def find_updated(language, namespace, console_output=False):
    """Find command pages which is updated in English wiki."""
    suffix = '-' + language + '-' + namespace

    print u'Getting pages and commands from cache'

    en_pages = Cache(Pages(namespace=namespace).get, 'pages-en-' + namespace)
    pages = Cache(Pages(namespace=namespace, language=language).get,
                  'pages' + suffix)

    en_commands = Cache(Commands(pages=en_pages.data).get, 'commands-en')
    commands = Cache(Commands(language, pages=pages.data).get,
                     'commands-' + language)

    # Updated pages
    msg = u'== Updated command pages ==\n'
    if console_output:
        print msg

    msg += u'{| class="wikitable"\n'
    msg += u'|- <!-- header -->\n'
    msg += u'! Page !! Last edit !! English page !! Last edit\n'

    row = 1
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
        link = page['fullTitle']
        time = page['editTime']
        en_title = en_page['title']
        en_link = en_page['fullTitle']
        en_time = en_page['editTime']
        if time < en_time:
            if console_output:
                # \r\x1b[50C - 50 chars right from start of line
                print u'{0} updated\r\x1b[50C{1}'.format(title, time)
                print u'{0} updated\r\x1b[50C{1}'.format(en_title, en_time)
                print u''
            msg += u'|- <-- row {0} -->\n'.format(row)
            row += 1
            msg += u'| [[{0}|{1}]] || {2}'.format(link, title, time)
            msg += (u'|| [[:en:{0}|{1}]] || {2}\n'
                    .format(en_link, en_title, en_time))

    msg += u'|}\n'

    return msg


def find_size_difference(language, namespace, console_output=False):
    """Find pages with large size difference."""
    suffix = '-' + language + '-' + namespace

    print u'Getting pages and commands from cache'

    en_pages = Cache(Pages(namespace=namespace).get, 'pages-en-' + namespace)
    pages = Cache(Pages(namespace=namespace, language=language).get,
                  'pages' + suffix)

    en_commands = Cache(Commands(pages=en_pages.data).get, 'commands-en')
    commands = Cache(Commands(language, pages=pages.data).get,
                     'commands-' + language)

    # Updated pages
    msg = u'== Size differences ==\n'
    if console_output:
        print msg
        print 'Title, largest, english title, difference.\n'

    msg += u'{| class="wikitable"\n'
    msg += u'|- <!-- header -->\n'
    msg += u'! Page !! Largest !! English page !! Size difference\n'

    size_differences = []
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
        link = page['fullTitle']
        size = len(page['text'])
        en_title = en_page['title']
        en_link = en_page['fullTitle']
        en_size = len(en_page['text'])
        difference = abs(size - en_size)
        if difference > 300:
            # ~ three sentences difference
            largest = '<--' if size > en_size else '-->'
            size_differences.append({
                'difference': difference,
                'largest': largest,
                'title': title,
                'link': link,
                'en_title': en_title,
                'en_link': en_link,
            })

    # sort after size, highest first
    size_differences.sort(key=lambda obj: obj['difference'], reverse=True)
    row = 1
    for obj in size_differences:
        if console_output:
            # \r\x1b[50C - 70 chars right from start of line
            print (u'{0} {1} {2}\r\x1b[70C{3} chars'
                   .format(obj['title'], obj['largest'], obj['en_title'],
                           obj['difference']))
            print u''
        msg += u'|- <-- row {0} -->\n'.format(row)
        row += 1
        msg += u'| [[{0}|{1}]]\n'.format(obj['link'], obj['title'])
        msg += u'| {0}\n'.format(obj['largest'])
        msg += u'| [[:en:{0}|{1}]]\n'.format(obj['en_link'], obj['en_title'])
        msg += u'| {0}\n'.format(obj['difference'])

    msg += u'|}\n'

    return msg


def wiki(language, namespace):
    """
    Run all reports and write result to wikipage 'Translation Report'.
    """

    site = pywikibot.Site(code=language, fam='geogebra')
    page = pywikibot.Page(site, 'Translation Report')

    page.text = find_missing(language, namespace)
    page.text += find_updated(language, namespace)
    page.text += find_size_difference(language, namespace)

    print (u'Saving to http://wiki.geogebra.org/{0}/Translation_Report'
           .format(language))
    page.save(comment='geogebra wiki translation helper')



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
        find_missing(language, namespace, True)
    elif cmd == 'updated':
        find_updated(language, namespace, True)
    elif cmd == 'size':
        find_size_difference(language, namespace, True)
    elif cmd == 'wiki':
        wiki(language, namespace)


if __name__ == '__main__':
    main()
