""" for testing stuff out """


from pywikibot import pagegenerators
import pywikibot
import pickle

from time import sleep

site = pywikibot.Site('en', fam='geogebra')
pages = pagegenerators.AllpagesPageGenerator(start='v', site=site, namespace=100, content=True)

print('generator made, sleep to see when/what is fetched') # seem to be nothing
sleep(3)
print('done sleeping')

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
    if i == 3:
        print obj
print('loop done')

f = open('data/page.dump', 'w')
pickle.dump(pagestore, f, -1)


#pywikibot.Page.editTime

#members = [attr for attr in dir(Example()) if not callable(attr) and not attr.startswith("__")]
