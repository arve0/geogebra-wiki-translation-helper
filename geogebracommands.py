from urllib import urlopen
import json
import codecs

class Commands:
    """ Class for commands """

    # Variables

    def __init__(self, language=None, languageCode=None):
        self.language = language or 'English'
        self.languageCode = languageCode or 'en'
        self.filename = 'data/commands-%s.json' % (self.languageCode,)

        # Infix codes
        if self.languageCode == 'nb':
            self.commandsInfix = '_no_NO'
        elif self.languageCode == 'nn':
            self.commandsInfix = '_no_NO_NY'
        elif self.languageCode != 'en':
            self.commandsInfix = '_' + self.languageCode
        else:
            self.commandsInfix = ''

    
    def getApiUrl(self):
        return 'https://geogebra.googlecode.com/svn/trunk/geogebra/desktop/geogebra/properties/command%s.properties' % (self.commandsInfix,)


    def convertRawDataToDictionary(self):
        """ Convert the raw data to a list of dictionaries """
        if self.languageCode != 'en':
            # raw data does not include names that are the same in english
            self.loadFromJson('data/commands-en.json')
        else: self.commands = {}
        lines = self.rawData.split('\n')
        for line in lines:
            translation = ''
            words = line.split('=')
            if '.Syntax' not in words[0]:
                translation = words[1]
            else:
                command = words[0].split('.')[0]
                if translation == '':
                    obj = { command: { 'syntax': words[1] } } # translation == english
                else:
                    obj = { command: {
                        'translation': translation,
                        'syntax': words[1]
                    }}
                self.commands.update(obj)


    def loadFromSvn(self):
        """ Load commands from SVN, convert raw data and store them to self.commands """
        print('Fetching from SVN...')
        self.rawData = urlopen(self.getApiUrl()).read().decode('ISO-8859-1')
        self.convertRawDataToDictionary()
      

    def saveToJson(self):
        """ Stores the data gotten from SVN to a json file. """
        print('Storing data to: ' + self.filename)
        object = {
            'language': self.language,
            'languageCode': self.languageCode,
            'commands': self.commands,
        }
        f = codecs.open(self.filename, 'w', encoding='utf8')
        jsonStr = json.dumps(object, ensure_ascii=False, encoding='utf8') # use utf-8 encoding(instead of escaped ascii), to make json files easy to read for humans
        f.write(jsonStr)
        f.close()


    def loadFromJson(self, filename=None):
        """ Loads data from json file. """
        if not filename:
            filename = self.filename
        print('Loading file ' + filename)
        f = codecs.open(filename, encoding='utf8')
        object = json.load(f)
        f.close()
        self.commands = object['commands']


    def printStatus(self):
        """ Prints number of commands in object. """
        print('Language: %s(%s), Number of commands: %i' % (self.language, self.languageCode, len(self.commands)) )
        
