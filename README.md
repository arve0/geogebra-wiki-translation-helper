# GeoGebra Wiki translation helper #
Scripts for helping translation of the GeoGebra manual on the [wiki](http://wiki.geogebra.org/).

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
git submodule update --init
cd pywikibot-core
sudo python setup.py install
```


## Usage ##

### Download wikipages to text files ###
```
./save.py language-code [namespace]
```
Saves pages to text files in existing directory 'pages'. Filename format is 'Title.lang.ns.wiki'. File encoding is UTF-8. Namespace is optional.

Default namespace is 'Manual' (applies for all commands). For empty namespace, use 'Main'.
#### Example ####
```
./save.py nb
```
Output:
```
Loading cache/pages-nb-Manual.json
Saving pages to text files.
```


### Upload text file to wiki ###
```
./upload.py [comment="optional comment"] filename(s)
```
Upload text files to wiki. Filename is used as title/pagename. Expexts filename format 'Title.lang.ns.wiki'. If several files is given, script will upload them in turn. Leading directory is stripped filenames. Comment is optional.
#### Example ####
```
./upload.py comment="fikset versjon" pages/Vektor\ Kommando.nb.Manual.wiki
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
Page [[Manual:Vektor Kommando]] saved
```


### Reports ###
```
./report.py command language-code [namespace]
```

#### Update cache ####

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
#### Generating report ####
This will generate a (wiki page)[http://wiki.geogebra.org/nb/Translation_Report] with all reports.
```
./report.py wiki nb
```
Output:
```
Getting pages and commands from cache
Loading cache/pages-nb-Manual.json
Loading cache/commands-nb.json
Getting pages and commands from cache
Loading cache/pages-en-Manual.json
Loading cache/pages-nb-Manual.json
Loading cache/commands-en.json
Loading cache/commands-nb.json
Saving to http://wiki.geogebra.org/nb/Translation_Report
Sleeping for 7.4 seconds, 2014-07-02 23:45:29
WARNING: API warning (main): Unrecognized parameter: 'assert'
Page [[Translation Report]] saved
```



#### Find missing pages ####
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

#### Find updated pages ####
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

## Requirements ##
Scripts are only tested on Mac OS X.

Forward slashes in titles is converted to backward slashes, which means that saving to text files will not work for windows file systems.
