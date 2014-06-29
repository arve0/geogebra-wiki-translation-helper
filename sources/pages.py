# -*- coding: utf-8 -*-
"""
File: pages.py
Author: Arve Seljebu
Email: arve.seljebu@gmail.com
Github: arve0
Description: Class Pages: Retrieve all pages from specified language and
             namespace. Return as list.
"""


from pywikibot import pagegenerators
import pywikibot
from language import Language
import re


class Pages(object):
    """
    Wikipages(data) gotten from pywikibot.
    """
    def __init__(self, namespace='Manual', language='en'):
        """
        Setup language, namespace, namespace_number and _site.

        Raises NameError if namespace not found in wiki or language not found
        in config.py.
        """
        self.language = Language(language.lower())
        self._site = pywikibot.Site(code=language, fam='geogebra')
        self.namespace = namespace.capitalize()
        # namespace_number requires _site
        self.namespace_number = self._get_namespace_number()
        self.pages = None


    def get(self):
        """
        Retrieve all pages from wiki. Return list of pages(dict).
        Page keys: id, title, text, revid, editTime, namespace, isRedirect.
        """
        # use Content=True (loads all pages in same query)
        pages = pagegenerators.AllpagesPageGenerator(
            site=self._site, namespace=self.namespace_number, content=True)

        self.pages = []
        print u'Getting pages from {0} wiki in namespace {1}.'\
                .format(self.language, self.namespace)
        for page in pages:
            title = self._strip_namespace(page.title())
            # capitalize without lower all other chars (ex: nPr Command)
            title = title.replace(title[0], title[0].upper(), 1)
            obj = {
                'id': page._pageid,
                'title': title,
                'text': page.text,
                'revid': page._revid,
                'editTime': page.editTime().toISOformat(),
                'namespace': page.namespace(),
                'isRedirect': page._isredir,
            }
            self.pages.append(obj)

        return self.pages


    def _get_namespace_number(self):
        """
        Sets integer for self.namespace to self.namespace_number.

        Raises NameError if not found.
        """
        # Special case - no namespace, lets call it main
        if self.namespace == 'Main':
            namespace = ''
        else:
            namespace = self.namespace

        namespace_number = self._site.ns_index(namespace)
        if namespace_number == None:
            raise NameError('ERROR: Namespace {0} not'.format(self.namespace) +\
                    ' found in "{0}" wiki.'.format(self.language))

        return namespace_number


    def _strip_namespace(self, title):
        """
        Returns title without Namespace:
        """
        # Special case, no namespace
        if self.namespace_number == 0:
            return title

        regex = re.compile('^{0}:'.format(self.namespace))
        title = re.sub(regex, '', title)
        return title


    def print_pages(self):
        """
        Prints titles to self.pages and beginning of page.text.
        """
        msg = 'Page titles'
        print msg
        print '='*len(msg)

        for page in self.pages:
            # Print title + beginning of text (strip until ;)
            print page['title'] + ':'
            start = page['text'].find(';')
            if start == -1:
                # match common start of "real" text:
                # line starting with A-Z, *, :
                # # (redirects)
                # {{lowercase
                match = re.search(r'(\n[A-Z*:]|#|\{\{[a-z])', page['text'])
                if match == None:
                    start = 0
                else:
                    start = match.span()[0]
            print page['text'][start:start+80].replace('\n', ' ')
