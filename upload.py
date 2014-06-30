#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: upload.py
Author: Arve Seljebu
Email: arve.seljebu@gmail.com
Github: arve0
Description: Upload page with text from file.
"""

import sys
import codecs
import pywikibot
import re

def print_usage():
    """Print usage of this script."""
    usage = '''
    Usage
    =====
    {0} [comment="commenting this upload"] file(s)

    Upload page(s) to wiki, with text from file(s). Filename is used for page
    title. Filename should be in format Title.lang.ns.wiki.
    Ex: 'Vector Command.en.Manual.wiki'

'''.format(sys.argv[0])
    print usage


def main():
    """Upload"""
    length = len(sys.argv)
    if length == 1:
        print_usage()
        sys.exit()

    comment = None

    regex_folders = r'[a-zA-Z]+\/'
    regex_end = r'\.([a-z]+)\.([A-Za-z]+)\.wiki'
    regex_comment = '^comment=(.+)'
    for filename in sys.argv[1:]:
        title = filename

        match = re.match(regex_comment, title)
        if match != None:
            comment = match.groups()[0]
            continue

        match = re.match(regex_folders, title)
        if match != None:
            #folder = filename[0:match.end()]
            #print 'Removing folder {0} from {1}'.format(folder, filename)
            title = title[match.end():]

        match = re.search(regex_end, title)
        if match == None:
            print 'Filename {0} not in correct format'.format(filename)
            print 'Should be title.lang.ns.wiki.'
            continue

        file_ = codecs.open(filename, encoding='utf8')
        text = file_.read()
        file_.close()

        print 'CONTENT:'
        print text

        title = title[0:match.start()].replace('\\', '/').decode('utf8')
        language = match.groups()[0]

        site = pywikibot.Site(code=language, fam='geogebra')

        namespace = match.groups()[1]
        if namespace == 'Main':
            namespace = ''
        namespace_number = site.ns_index(namespace)

        page = pywikibot.Page(source=site, title=title, ns=namespace_number)

        if comment == None:
            comment = 'Uploaded from geogebra-wiki-translation-helper'

        print 'UPLOADING..'
        page.text = text
        page.save(comment=comment)


if __name__ == '__main__':
    main()
