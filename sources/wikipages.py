"""
File: wikipages.py
Author: Arve Seljebu
Email: arve.seljebu@gmail.com
Github: arve0
Description: Class wich fetch all pages from mediawiki.
"""


import json
from urllib import urlopen
from urllib import urlencode
from time import sleep
import codecs


class WikiPages(object):
    """ Class for wikipages """

    # variables
    start_letter = 'a'       # where to start from when getting pages, should be the first letter in the alphabet


    def __init__(self, language=None, language_code=None):
        self.language = language or 'English'
        self.language_code = language_code or 'en'
        self.filename = 'data/wikipages-%s.json' % (self.language_code,)


    def get_api_url(self):
        """ Returns the the API URL we are working on """
        return 'http://wiki.geogebra.org/s/%s/api.php' % (self.language_code,)


    def get_all_pages_url(self, start_letter):
        params = urlencode({
            'action': 'query',
            'list': 'allpages',
            'apfrom': start_letter,
            'aplimit': 5000,
            'format': 'json',
        })
        return self.get_api_url() + '?%s' % (params,)


    def load_from_wiki(self):
        """ Loads pages from mediawiki API, starting from self.start_letter, and stores them to self.pages """
        message = 'Getting pages from wiki. Language: %s(%s)' % (self.language,self.language_code)
        print message
        query = {}
        query['query-continue'] = { 'allpages': { 'apcontinue': self.start_letter }}
        pages = []

        while 'query-continue' in query.keys():
            s = query['query-continue']['allpages']['apcontinue']
            url = self.get_all_pages_url(start_letter=s)
            response = urlopen(url).read()
            sleep(1) # being nice to the webserver
            query = json.loads(response)
            pages.extend(query['query']['allpages'])

        self.pages = pages
        message = 'Done. Got %i pages.' % (len(pages),)
        print message

    def print_status(self):
        """ Prints number of pages in object. """
        message = 'Language: %s(%s), Number of pages: %i' % (self.language, self.language_code, len(self.pages))
        print message


    def save_to_json(self):
        """ Stores the data gotten from the wiki to a json file. """
        print 'Storing data to: ' + self.filename
        object = {
            'language': self.language,
            'language_code': self.language_code,
            'pages': self.pages,
        }
        f = codecs.open(self.filename, 'w', encoding='utf8')
        f.write(json.dumps(object))
        f.close()


    def load_from_json(self):
        """ Loads data from json file. """
        print 'Loading file ' + self.filename
        f = codecs.open(self.filename, encoding='utf8')
        object = json.load(f)
        f.close()
        self.pages = object['pages']
