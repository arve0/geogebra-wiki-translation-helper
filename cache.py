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


def _filename(namespace=0, language='en'):
    """
    Returns filename for pickle
    """

    return 'data/pages-' + str(namespace) + '-' + language + '.pickle'


def _check_params(namespace, language):
    """
    Checks if params is OK.
    """

    lang_ok = False
    namespace = True # TODO
    for lang in config.LANGUAGES:
        if lang.code == language:
            lang_ok = True

    if not lang_ok: # TODO namespace
        print 'Language ' + language + ' not in config. Please add it to config.py'

    return lang_ok and namespace

def _print_usage():
    """
    Prints usage of this file as a script.
    """

    print 'Usage:'
    print sys.argv[0] + '\n'
    print 'get [namespace] [language] \t- get all pages from wiki and store to pickle'
    print 'show [namespace] [language] \t- print all page titles from cache\n'
    print 'Default values:'
    print 'namespace: 0'
    print 'language: en'


def _call(function, args):
    """
    Helper function to call function with right amount of args.
    """

    if len(args) == 4:
        function(int(args[2]), args[3])
    elif len(args) == 3:
        function(int(args[2]))
    elif len(args) == 2:
        function()
    else:
        _print_usage()

    
def get_from_wiki(namespace=0, language='en'):
    """
    Retrieve all pages from specified namespace, save to pickle
    (data/pages-namespace-languagecode.pickle) and return list of pages.
    """

    if not _check_params(namespace, language):
        return

    site = pywikibot.Site(language, fam='geogebra')
    pages = pagegenerators.AllpagesPageGenerator(site=site, namespace=namespace, content=True)

    pagestore = []
    print 'Getting pages from wiki in namespace ' + str(namespace) + ' and language ' + language
    for page in pages:
        obj = {
            'id': page._pageid,
            'title': page.title(),
            'text': page.text,
            'timestamp': page._timestamp, # useful?
            'revid': page._revid,
            'editTime': page.editTime(),
            'namespace': page.namespace(),
            'isRedirect': page._isredir,
        }
        pagestore.append(obj)

    filename = _filename(namespace, language)
    print 'Saving pages to ' + filename
    try:
        file_ = open(filename, 'w')
        pickle.dump(pagestore, file_, -1)
        file_.close()
    except IOError as (errno, strerror):
        print 'I/O error({0}): {1}'.format(errno, strerror)
    except ValueError:
        print 'Could not convert data to an integer.'
    except:
        print 'Unexpected error:', sys.exc_info()[0]
        raise

    return pages


def get_from_cache(namespace=0, language='en'):
    """
    Returns list of pages from pickle cache.
    """

    if not _check_params(namespace, language):
        return

    filename = _filename(namespace, language)
    file_ = open(filename)
    pages = pickle.load(file_)
    file_.close()

    return pages


def print_pickle(*args):
    """
    Prints all page titles in pickle.
    """

    msg = 'Pages in cache'
    print msg
    print '='*len(msg)

    pages = get_from_cache(*args)
    for page in pages:
        print page['title']


def main(args):
    """
    If called as script.
    """

    if 'get' in args:
        _call(get_from_wiki, args)
    elif 'show' in args:
        _call(print_pickle, args)
    else:
        _print_usage()


if __name__ == '__main__':
    main(sys.argv)
