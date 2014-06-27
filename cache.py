"""
File: cache.py
Author: Arve Seljebu
Email: arve.seljebu@gmail.com
Github: arve0
Description: Class Cache: Reads cache/filename.json upon initialization, if not
             found use getter. Data is available in self.data. Stores self.data
             to cache/filename.json upon deletion/destruction.
"""

import codecs
import json

class Cache(object):
    """
    Holds data and stores it to filename upon deletion/destruction. Then read
    it from cache upon next initialization.
    """

    def __init__(self, getter, filename):
        """
        Set up self.data. Get data from cache/filename.json or getter.

        :getter: Source of data. Should return data which is possible to
                 serialize to JSON (dict, list, etc).
        :filename: Part of filename for cache. Full filename is
                   cache/filename.json. Should be unique to avoid clashes.
        """

        self._getter = getter
        self._filename = u'cache/{0}.json'.format(filename)
        self.data = None

        try:
            self.load()
        except IOError:
            self.get()



    def get(self):
        """ Get data to self.data from self._getter. """

        self.data = self._getter()



    def load(self):
        """ Load self._filename to self.data. """

        print 'Loading {0}'.format(self._filename)
        file_ = codecs.open(self._filename, encoding='utf8')
        self.data = json.load(file_)
        file.close()



    def save(self):
        """ Save self.data to self._filename. """

        print u'Saving cache: {0}'.format(self._filename)
        file_ = codecs.open(self._filename, 'w', encoding='utf8')
        # make json files easy to read, use indention + utf8 encoding
        jsonstr = json.dumps(self.data, ensure_ascii=False, encoding='utf8',
                             sort_keys=True, indent=4)
        file_.write(jsonstr)
        file_.close()



    def __del__(self):
        """ Save cache upon deletion/destruction. """

        self.save()
