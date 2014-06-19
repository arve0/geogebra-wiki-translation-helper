import json
from urllib import urlopen
from urllib import urlencode
from time import sleep
import codecs


class WikiPages:
    """ Class for wikipages """

    # variables
    startLetter = 'a'       # where to start from when getting pages, should be the first letter in the alphabet


    def __init__(self, language=None, languageCode=None):
        self.language = language or 'English'
        self.languageCode = languageCode or 'en'
        self.filename = 'data/wikipages-%s.json' % (self.languageCode,)


    def getApiUrl(self):
        """ Returns the the API URL we are working on """
        return 'http://wiki.geogebra.org/s/%s/api.php' % (self.languageCode,)


    def getAllPagesUrl(self, startLetter):
        params = urlencode({
            'action': 'query',
            'list': 'allpages',
            'apfrom': startLetter,
            'aplimit': 5000,
            'format': 'json',
        })
        return self.getApiUrl() + '?%s' % (params,)


    def loadFromWiki(self):
        """ Loads pages from mediawiki API, starting from self.startLetter, and stores them to self.pages """
        print('Getting pages from wiki. Language: %s(%s)' % (self.language,self.languageCode))
        query = {}
        query['query-continue'] = { 'allpages': { 'apcontinue': self.startLetter }}
        pages = []

        while 'query-continue' in query.keys():
            s = query['query-continue']['allpages']['apcontinue']
            url = self.getAllPagesUrl(startLetter=s)
            response = urlopen(url).read()
            sleep(1) # being nice to the webserver
            query = json.loads(response)
            pages.extend(query['query']['allpages'])

        self.pages = pages
        print('Done. Got %i pages.' % (len(pages),) )


#    def loadLanguageLinksFromWiki(self, titles=['Main Page']):
#        """ Load language links from wiki. """
#        params = urlencode({
#            'action': 'query',
#            'prop': 'langlinks',
#            'lllimit': 500,
#            'titles': '|'.join(titles),
#            'format': 'json',
#        })
#        response = urlopen(url, params).read()
#        sleep(1)
#        query = json.loads(response)['query']
#        pages = query['pages']
#        links = []
#        for pageId, page in pages.iteritems():
#            links.append(page)
#        return links


    def printStatus(self):
        """ Prints number of pages in object. """
        print('Language: %s(%s), Number of pages: %i' % (self.language, self.languageCode, len(self.pages)) )


    def saveToJson(self):
        """ Stores the data gotten from the wiki to a json file. """
        print('Storing data to: ' + self.filename)
        object = {
            'language': self.language,
            'languageCode': self.languageCode,
            'pages': self.pages,
        }
        f = codecs.open(self.filename, 'w', encoding='utf8')
        f.write(json.dumps(object))
        f.close()


    def loadFromJson(self):
        """ Loads data from json file. """
        print('Loading file ' + self.filename)
        f = codecs.open(self.filename, encoding='utf8')
        object = json.load(f)
        f.close()
        self.pages = object['pages']
