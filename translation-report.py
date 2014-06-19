#!/usr/bin/env python
# -*- coding: utf-8 -*

import sys
from wikipages import WikiPages
from geogebracommands import Commands

class Bunch:
    # http://code.activestate.com/recipes/52308-the-simple-but-handy-collector-of-a-bunch-of-named/
    # save typing, instead of dictionaries
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

# global variables
languages = [
    Bunch(name='English',code='en'),
    Bunch(name='Norsk bokmål', code='nb'),
    Bunch(name='Norsk nynorsk', code='nn'),
]
pagesDict = {}
commandsDict = {}


def initializePages():
    """ Set up pagesDict """
    for language in languages:
        pagesDict[language.code] = WikiPages(language.name, language.code)
    

def getAndStoreWikiPages():
    """ Get list of all pages and store it to json """

    initializePages()
    for language in languages:
        pagesDict[language.code].loadFromWiki()
        pagesDict[language.code].saveToJson()
    

def getWikiPagesFromDisk():
    """ Get wiki pages from json """

    initializePages()
    for language in languages:
        pagesDict[language.code].loadFromJson()


def initializeCommands():
    """ Set up commandsDict """
    for language in languages:
        commandsDict[language.code] = Commands(language.name, language.code)
    

def getAndStoreCommands():
    """ Get commands from svn and store to disk """

    initializeCommands()
    for language in languages:
        commandsDict[language.code].loadFromSvn()
        commandsDict[language.code].saveToJson()


def getCommandsFromDisk():
    """ Get commands from json files """

    initializeCommands()
    for language in languages:
        commandsDict[language.code].loadFromJson()


def analyzeMissingPages():
    """ Find missing pages (not translated from english) """
    header = 'Loading from disk'
    print(header)
    print('='*len(header))
    getWikiPagesFromDisk()
    getCommandsFromDisk()
    print('')

    header = 'Number of pages'
    print(header)
    print('='*len(header))
    for language in languages:
        pagesDict[language.code].printStatus()
        commandsDict[language.code].printStatus()
        i = 0
        cmd = []
        for page in pagesDict[language.code].pages:
            for command in commandsDict[language.code].commands:
                if command in page['title']:
                    i += 1
                    cmd.append(page['title'])
        print i
    print('')





def main(argv):
    if 'get-wiki' in argv:
        getAndStoreWikiPages()
    elif 'get-commands' in argv:
        getAndStoreCommands()
    elif 'analyze' in argv:
        analyzeMissingPages()
    else:
        print('Usage:')
        print(argv[0] + ' analyze - reads data from json and analyzes it')
        print(argv[0] + ' get-commands - gets a list of all command commands from SVN and stores it to a json file')
        print(argv[0] + ' get-wiki - gets a list of all pages from wiki and stores it to a json file')

if __name__ == '__main__':
    main(sys.argv)

# hent alle linker
#url = apiUrl('en')
#titles = []
#links = []
#response = ''
#for (counter, page) in enumerate(enPages):
#    titles.append(page['title'].encode('utf-8'))
#    if (counter+1)%50 == 0: # get no more then 50 pages/links
#        tempLinks = getLinks(titles)
#        print type(tempLinks)
#        titles = []
#    elif (counter+1) == len(enPages):
#        links.extend(getLinks(titles))
#        titles = []

# todo - check norwegian links
# todo - get data from translate app: http://dev.geogebra.org/ggbtrans/props/view/
