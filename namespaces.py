#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: namespaces.py
Author: Arve Seljebu
Email: arve.seljebu@gmail.com
Github: arve0
Description: List all namespaces in given language.
"""

from pywikibot import Site
import sys
from language import Language

# utf8 hack
# http://stackoverflow.com/questions/492483/setting-the-correct-encoding-when-piping-stdout-in-python
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

if __name__ == '__main__':
    main()

def main():
    """Print all namespaces in given language to console."""
    length = len(sys.argv)
    if length == 1:
        language = Language('en')
    else:
        language = Language(sys.argv[1])

    site = Site(language.code, 'geogebra')
    print u'== Namespaces in {} =='.format(language)
    for number, names in site.namespaces().iteritems():
        names_print = ', '.join(names)
        print u'Number: {0}\t Names: {1}'.format(number, names_print)
