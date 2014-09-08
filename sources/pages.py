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
from properties import capitalize


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
        self.namespace = capitalize(namespace)
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
        print (u'Getting pages from {0} wiki in namespace {1}.'
               .format(self.language, self.namespace))
        for page in pages:
            obj = {
                'id': page._pageid,
                'title': page.title(withNamespace=False),
                'fullTitle': page.title(),
                'text': page.text,
                'revid': page._revid,
                'editTime': page.editTime().toISOformat(),
                'date': page.editTime().toISOformat()[0:10],
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

        en_site = pywikibot.Site('en', 'geogebra')
        namespace_number = en_site.ns_index(namespace)

        if namespace_number == None:
            raise NameError(u'Namespace {0} not found in english wiki.'
                            .format(self.namespace).encode('utf8'))

        return namespace_number


    def print_pages(self):
        """
        Prints titles to self.pages and beginning of page.text.
        """
        msg = 'Page titles'
        print msg
        print u'='*len(msg)

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
