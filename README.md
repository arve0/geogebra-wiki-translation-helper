# GeoGebra Wiki translation helper #
Scripts for helping translation of the GeoGebra manual on the [wiki](http://wiki.geogebra.org/). See one of the reports here: http://wiki.geogebra.org/nb/Translation_Report

Current features:
- Generating reports
    - Finding updated wikipages in english
    - Finding missing pages
- Editing from text files
    - use your favorite text editor
- Uploading from text files

Uses cache to avoid server and bandwidth strain. **Remember** to update cache once in a while! `./report.py cache language-code`


## Install ##
```
git clone https://github.com/arve0/geogebra-wiki-translation-helper.git
cd geogebra-wiki-translation-helper
git submodule update --init
cd pywikibot-core
sudo python setup.py install
sudo chown -R $(whoami) ~/.pywikibot
```
In the piwikibot setup, use these options:
k, n, y, 4, YOUR_LANGUAGE, YOUR_WIKI_USERNAME, s, n, n.

Example:
```
Your default user directory is "/Users/arve/.pywikibot"
How to proceed? ([K]eep [c]hange) K
Do you want to copy user files from an existing pywikibot installation? n
Create user-config.py file? Required for running bots ([y]es, [N]o) y
1: anarchopedia
2: battlestarwiki
3: commons
4: geogebra
5: i18n
6: incubator
7: lockwiki
8: lyricwiki
9: mediawiki
10: meta
11: omegawiki
12: osm
13: outreach
14: species
15: strategy
16: test
17: vikidia
18: wikia
19: wikibooks
20: wikidata
21: wikimedia
22: wikinews
23: wikipedia
24: wikiquote
25: wikisource
26: wikitech
27: wikiversity
28: wikivoyage
29: wiktionary
30: wowwiki
Select family of sites we are working on, just enter the number not name (default: wikipedia): 4
This is the list of known language(s):
bs ca cs da de el en es et fa fr gl he hi hr hu is it kk ko lt mk nb nn pl pt ru sk sl sr sv tr zh
The language code of the site we're working on (default: 'en'): nb
Username (nb geogebra): arve
Which variant of user_config.py:
[S]mall or [E]xtended (with further information)? S
Do you want to add any other projects? (y/N)n
'/Users/arve/.pywikibot/user-config.py' written.
Create user-fixes.py file? Optional and for advanced users ([y]es, [N]o) n
```


## Example of workflow ##
```
./report.py cache en    # cache English pages
./report.py cache nb    # cache Norwegian pages
./save.py nb            # save Norwegian pages to folder 'pages'
grep -l "{{translate" pages/*   # list pages which aren't translated
mkdir translate         # make directory
                        # move pages with pattern to translate directory
grep -l --null "{{translate" pages/* | xargs -0 -J % mv % translate
vim translate/*         # do work with your favorite editor
                        # upload translated pages to wiki
./upload.py comment="translated from english" translate/*
```

## Usage ##

### Download wikipages to text files ###
```
./save.py language-code [namespace]
```
Saves pages to text files in existing directory 'pages'. Filename format is 'Title.lang.ns.wiki'. File encoding is UTF-8. Namespace is optional.

Default namespace is 'Main' (applies for all commands). For empty namespace, use 'Main'.
#### Example ####
```
./save.py nb
```
Output:
```
Loading cache/pages-nb-Main.json
Saving pages to text files.
```


### Upload text file to wiki ###
```
./upload.py [comment="optional comment"] filename(s)
```
Upload text files to wiki. Filename is used as title/pagename. Expexts filename format 'Title.lang.ns.wiki'. If several files is given, script will upload them in turn. Leading directory is stripped filenames. Comment is optional.
#### Example ####
```
./upload.py comment="fikset versjon" pages/Vektor\ Kommando.nb.Main.wiki
```
Output:
```
CONTENT:
<noinclude>{{Manual Page|version=4.4}}</noinclude>{{command|vector-matrix|Vektor}}
{{unchecked}}

;Vektor[ <Punkt> ]
:Returnerer posisjonsvektoren til punktet. Det vil si vektoren fra origo til punktet.
;Vektor[ <Startpunkt A>, <Sluttpunkt B> ]
:Returnerer vektoren som starter i ''A'' og slutter i ''B''.

{{note|Se også verktøyet [[image:Tool Vector between Two Points.gif]] [[Vektor mellom to punkt Verktøy|Vektor mellom to punkt]].}}

{{betamanual|version=5.0|
{{Note|1=Fra GeoGebra 5 vil denne kommandoen også kunne brukes i 3D.}}
}}

UPLOADING..
Sleeping for 8.2 seconds, 2014-06-30 22:58:13
WARNING: API warning (main): Unrecognized parameter: 'assert'
Page [[Vektor Kommando]] saved
```


### Reports ###
```
./report.py command language-code [namespace]
```
Available commands:
* cache
* missing
* size
* updated
* wiki

#### cache command ####
Will download wiki and save it to "cache" directory.

```
./report.py cache nb
```
Output:
```
Updating cache for Norsk bokmål(nb), namespace Main
=====================================================
Getting pages from Norsk bokmål(nb) wiki in namespace Main.
Fetching Norsk bokmål(nb) commands from SVN.
Saving cache: cache/pages-nb-Main.json
Saving cache: cache/commands-nb.json
```
#### wiki command ####
This will generate a [wiki page](http://wiki.geogebra.org/nb/Translation_Report) with all reports.
```
./report.py wiki nb
```
Output:
```
Getting pages and commands from cache
Loading cache/pages-nb-Main.json
Loading cache/commands-nb.json
Getting pages and commands from cache
Loading cache/pages-en-Main.json
Loading cache/pages-nb-Main.json
Loading cache/commands-en.json
Loading cache/commands-nb.json
Saving to http://wiki.geogebra.org/nb/Translation_Report
Sleeping for 7.4 seconds, 2014-07-02 23:45:29
WARNING: API warning (main): Unrecognized parameter: 'assert'
Page [[Translation Report]] saved
```



#### missing command ####
This will find missing wiki pages (commands, tools and articles defined in GeoGebra source code).
```
./report.py missing nb
```
Output:
```
Missing command pages in Norsk bokmål(nb), namespace Main
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

#### Find updated pages ####
```
./report.py updated nb
```
Output:
```
Updated command pages in Norsk bokmål(nb), namespace Main
===========================================================
Reg Kommando updated                              2012-12-30
Fit Command updated                               2013-08-26

Strekk Kommando updated                           2011-09-26
Stretch Command updated                           2013-07-18

GjennomsnittX Kommando updated                    2012-11-06
MeanX Command updated                             2013-05-03

GjennomsnittY Kommando updated                    2012-11-06
MeanY Command updated                             2013-05-03

Delingsforhold Kommando updated                   2012-10-05
AffineRatio Command updated                       2013-06-14
...
```

#### Find size difference in pages ####
```
./report.py size nb
```
Output:
```
== Size differences ==

Title, largest, english title, difference.

SpillLyd Kommando --> PlaySound Command                               4205 chars

LøsODE Kommando --> SolveODE Command                                  3848 chars

FordelingBinomial Kommando --> BinomialDist Command                   2667 chars
```

## Requirements ##
Scripts are only tested on Mac OS X, but should work on any OS. If you are unable to make it work, open an issue here on Github.
