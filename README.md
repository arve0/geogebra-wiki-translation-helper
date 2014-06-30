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
```
./report.py command language-code
```
### Update cache ###

```
./report.py cache nb
```
Output:
```
Updating cache for Norsk bokmål(nb), namespace Manual
=====================================================
Getting pages from Norsk bokmål(nb) wiki in namespace Manual.
Fetching Norsk bokmål(nb) commands from SVN.
Saving cache: cache/pages-nb-Manual.json
Saving cache: cache/commands-nb.json
```

### Find missing pages ###
```
./report.py missing nb
```
Output:
```
Getting pages and commands to work with
=======================================
Loading cache/pages-en-Manual.json
Loading cache/pages-nb-Manual.json
Loading cache/commands-en.json
Loading cache/commands-nb.json

Missing command pages in Norsk bokmål(nb), namespace Manual
===========================================================
Wikipage missing for command Polyeder
Wikipage missing for command KøyrKlikkScript
Wikipage missing for command TangentThroughPoint
Wikipage missing for command GroebnerLexDeg
Wikipage missing for command ErKonsyklisk
Wikipage missing for command SkilpaddeFram
Wikipage missing for command Kjegle
Wikipage missing for command Topp
...
```

### Find updated pages ###
```
./report.py updated nb
```
Output:
```
Getting pages and commands to work with
=======================================
Loading cache/pages-en-Manual.json
Loading cache/pages-nb-Manual.json
Loading cache/commands-en.json
Loading cache/commands-nb.json

Updated command pages in Norsk bokmål(nb), namespace Manual
===========================================================
Reg Kommando updated                              2012-12-30T14:50:41Z
Fit Command updated                               2013-08-26T13:01:13Z

Strekk Kommando updated                           2011-09-26T23:56:16Z
Stretch Command updated                           2013-07-18T08:02:38Z

GjennomsnittX Kommando updated                    2012-11-06T09:36:19Z
MeanX Command updated                             2013-05-03T13:21:49Z

GjennomsnittY Kommando updated                    2012-11-06T09:41:06Z
MeanY Command updated                             2013-05-03T13:14:44Z

Delingsforhold Kommando updated                   2012-10-05T09:55:59Z
AffineRatio Command updated                       2013-06-14T10:00:22Z
...
```
