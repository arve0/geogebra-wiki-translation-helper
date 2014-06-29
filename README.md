# GeoGebra Wiki translation helper #
This code will help in the translation work of the wiki by generating useful reports.


## Install ##
```
git clone https://github.com/arve0/geogebra-wiki-translation-helper.git
git submodule update --init
cd pywikibot-core
sudo python setup.py install
```

## Using ##
### Update cache ###

```
./report.py cache language-code
```

### Find missing pages ###
```
./report.py missing language-code
```

