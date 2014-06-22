#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: cache.py
Author: Arve Seljebu
Email: arve.seljebu@gmail.com
Github: arve0
Description: Retrieve all pages from specified namespace,
             and save to pickle (data/pages-namespace-languagecode.pickle).
"""


from pywikibot import pagegenerators
import pywikibot
import pickle
import config
import sys
import re


class PagesCache(object):
    """
    Abstraction for wikipages, from wiki or pickle cache.

    Raises NameError if namespace not found in wiki or language not found
    in config.py.
    """
    def __init__(self, namespace='Manual', language='en'):
        self.namespace = namespace.lower().capitalize()
        self.language = language.lower()
        self._check_language()
        self._site = pywikibot.Site(code=language, fam='geogebra')
        self.namespace_number = self._get_namespace_number()
        self.filename = self._get_filename()
        self.pages = None


    def get_from_wiki(self):
        """
        Retrieve all pages from specified namespace, save to pickle
        (data/pages-namespace-languagecode.pickle) and return list of pages.

        Raises IOError upon write error.
        """


        pages = pagegenerators.AllpagesPageGenerator(
            site=self._site, namespace=self.namespace_number, content=True)

        self.pages = []
        print 'Getting pages from wiki in namespace ' + self.namespace + \
                ' and language ' + self.language
        for page in pages:
            obj = {
                'id': page._pageid,
                'title': self._strip_namespace(page.title()),
                'text': page.text,
                'timestamp': page._timestamp, # useful?
                'revid': page._revid,
                'editTime': page.editTime(),
                'namespace': page.namespace(),
                'isRedirect': page._isredir,
            }
            self.pages.append(obj)

        print 'Saving pages to ' + self.filename
        file_ = open(self.filename, 'w')
        pickle.dump(self.pages, file_, -1)
        file_.close()

        return self.pages


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


    def get_from_cache(self):
        """
        Returns list of pages from pickle cache self.filename.

        Raises IOError upon file not found.
        """

        print 'Reading pages from ' + self.filename
        file_ = open(self.filename)
        self.pages = pickle.load(file_)
        file_.close()

        return self.pages


    def _get_filename(self):
        """
        Returns filename for pickle
        """

        filename = 'data/pages-{0}-{1}.pickle'\
                .format(self.namespace_number, self.language)
        return filename


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


    def _check_language(self):
        """
        Checks if language is in config.py. Raises NameError if not found.

        Raises NameError if not found.
        """

        lang_ok = False
        for lang in config.LANGUAGES:
            if lang.code == self.language:
                lang_ok = True

        if not lang_ok:
            raise NameError('ERROR: Language ' + self.language + \
                    ' not in config. Please add it to config.py')


    def print_(self):
        """
        Prints all page titles.
        """

        msg = 'Pages in cache'
        print msg
        print '='*len(msg)

        for page in self.pages:
            # Print title + beginning of text (strip until ;)
            print page['title'] + ':'
            start = page['text'].find(';')
            if start == -1:
                # match line starting with A-Z, * or :
                # match # (redirects)
                # match {{lowercase
                match = re.search('(\n[A-Z*:]|#|\{\{[a-z])', page['text'])
                if match == None:
                    start = 0
                else:
                    start = match.span()[0]
            print page['text'][start:start+80].replace('\n', ' ')

# for running as a script
def _print_usage():
    """
    Prints usage of this file as a script.
    """

    usage = '''
    Usage:
    {0} command [language] [namespace]

    Commands:
    get \t- get all pages from wiki and store to pickle
    show \t- print all page titles from cache

    Default values:
    language: en (language.code in config.py)
    namespace: manual
    
    To get default/empty namespace, use main. Ex: {0} show main
    '''.format(sys.argv[0])

    print usage
    sys.exit()


def _setup_pages(args):
    """
    Helper function to set up PageCache object.
    """

    pages = None
    if len(args) == 4:
        pages = PagesCache(language=args[2], namespace=args[3])
    elif len(args) == 3:
        pages = PagesCache(language=args[2])
    elif len(args) == 2:
        pages = PagesCache()
    elif len(args) > 5:
        raise Exception('ERROR: Wrong number of arguments. Got ' + \
                '{0}, expected 1-3.'.format(len(args)-1))

    return pages


def main(args):
    """
    If called as script.
    """

    try:
        pages = _setup_pages(args)

        # does not catch all, but is sufficient
        if 'get' in args:
            pages.get_from_wiki()
        elif 'show' in args:
            pages.get_from_cache()
            pages.print_()
        else:
            _print_usage()
    except IOError as error:
        print 'I/O ERROR: {0}'.format(error)
    except NameError as error:
        print format(error)
    except Exception as error:
        print format(error)
        raise # raise exception for debugging


if __name__ == '__main__':
    main(sys.argv)
