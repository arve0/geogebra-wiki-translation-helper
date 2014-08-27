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
import os

def print_usage():
    """Print usage of this script."""
    usage = '''
    Usage
    =====
    {0} [comment="commenting this upload"] file(s)

    Upload page(s) to wiki, with text from file(s). Filename is used for page
    title. Filename should be in format Title.lang.ns.wiki.
    Ex: 'Vector Command.en.Main.wiki'

'''.format(sys.argv[0])
    print usage


def main():
    """Upload"""
    length = len(sys.argv)
    if length == 1:
        print_usage()
        sys.exit()

    comment = None

    suffix = r'\.([a-z]+)\.([A-Za-z]+)\.wiki'
    comment_match = '^comment=(.+)'
    for filename in sys.argv[1:]:
        match = re.match(comment_match, filename)
        if match:
            comment = match.groups()[0]
            continue

        title = os.path.split(filename)[1]

        match = re.search(suffix, title)
        if not match:
            print u'Filename {0} not in correct format'.format(filename)
            print u'Should be title.lang.namespace.wiki.'
            continue

        file_ = codecs.open(filename, encoding='utf8')
        content = file_.read()
        file_.close()

        print 'CONTENT:'
        print content

        title = title[0:match.start()].replace('\\', '/').decode('utf8')
        language = match.groups()[0]
        namespace = match.groups()[1]
        if namespace == 'Main':
            namespace = ''

        site = pywikibot.Site(code=language, fam='geogebra')
        en_site = pywikibot.Site('en', 'geogebra')
        namespace_number = en_site.ns_index(namespace)

        page = pywikibot.Page(source=site, title=title, ns=namespace_number)

        if not comment:
            comment = 'Uploaded from geogebra-wiki-translation-helper'

        print 'UPLOADING..'
        page.text = content
        page.save(comment=comment)


if __name__ == '__main__':
    main()
