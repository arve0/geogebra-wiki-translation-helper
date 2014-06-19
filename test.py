#!/usr/bin/env python
# -*- coding: utf-8 -*

import pywikibot

site = pywikibot.Site(code='nb')
page = pywikibot.Page(site, 'Hovedside')
print(page.text)
