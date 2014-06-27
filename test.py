#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" for testing stuff out """


from pywikibot import pagegenerators
import pywikibot
from cache import Cache
import re

def strip_namespace(title, namespace):
    """
    Returns title without Namespace:
    """

    # Special case, no namespace
    if namespace == '':
        return title

    regex = re.compile('^{0}:'.format(namespace))
    title = re.sub(regex, '', title)
    return title

def get_pages():
    """
    Retrieve all pages from specified namespace, save to json
    (data/pages-namespace-languagecode.json) and return list of pages.

    Raises IOError upon write error.
    """

    site = pywikibot.Site(code='en',fam='geogebra')
    pagegen = pagegenerators.AllpagesPageGenerator(
        site=site, namespace=100, content=True)

    pages = []
    for page in pagegen:
        obj = {
            'id': page._pageid,
            'title': strip_namespace(page.title(), 'Manual'),
            'text': page.text,
            'revid': page._revid,
            'namespace': page.namespace(),
            'isRedirect': page._isredir,
        }
        pages.append(obj)

    return pages

Cache(get_pages, 'pages-100-en')
