#!/usr/bin/env python
# -*- coding: utf-8 -*

import sys
from WikiPages import WikiPages


class Bunch:
    # http://code.activestate.com/recipes/52308-the-simple-but-handy-collector-of-a-bunch-of-named/
    # save typing, instead of dictionaries
    def __init__(self, **kwds):
        self.__dict__.update(kwds)




a = Bunch()
a.name = { 'obj': 123, 'asdf': 'asd' }

print a.name['obj']
