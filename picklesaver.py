#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
File: picklesaver.py
Author: Arve Seljebu
Email: arve.seljebu@gmail.com
Github: arve0
Description: Retrieve all pages in specified namespace and
             save to a pickle (data/pages-languagecode.pickle)
"""


from pywikibot import pagegenerators
import pywikibot
import pickle


def main():
    """ Runs upon script execution """
    site = pywikibot.Site('en', fam='geogebra')
    pages = pagegenerators.AllpagesPageGenerator(site=site, namespace=100, content=True)

    pagestore = []
    for (i, page) in enumerate(pages):
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

    try:
        file_ = open('data/pages-en.pickle', 'w')
        pickle.dump(pagestore, file_, -1)
        file_.close()
    except:
        print ''
    finally:
        pass


if __name__ == '__main__':
    main()
