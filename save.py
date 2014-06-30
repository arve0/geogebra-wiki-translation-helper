#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: save.py
Author: Arve Seljebu
Email: arve.seljebu@gmail.com
Github: arve0
Description: Iterates through pages and save them to page/title.lang.wiki.
"""

import sys
import codecs
from cache import Cache
from sources import Pages


def print_usage():
    """Print usage of this script."""
    usage = '''
    Usage
    =====
    {0} language [namespace]

    Saves page.text to files in folder pages. Filename is title.language-code.wiki

    Default values
    ==============
    namespace: 'Manual'
'''.format(sys.argv[0])
    print usage


def main():
    """Save all pages in pages/title.lang.wiki"""
    length = len(sys.argv)
    if length == 3:
        language = sys.argv[1].lower()
        namespace = sys.argv[2].capitalize()
    elif length == 2:
        language = sys.argv[1].lower()
        namespace = 'Manual'
    else:
        print_usage()
        sys.exit()

    suffix = '-' + language + '-' + namespace
    pages = Cache(Pages(namespace=namespace, language=language).get,
                  'pages' + suffix)

    print 'Saving pages to text files.'
    for page in pages.data:
        t = page['title'].replace('/', '\\')
        filename = u'pages/' + t + '.' + language + '.' + namespace + '.wiki'
        file_ = codecs.open(filename, 'w', encoding='utf8')
        file_.write(page['text'])
        file_.close()

if __name__ == '__main__':
    main()

