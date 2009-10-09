#!/usr/bin/env python

"""
Python Interface to Google's translation API.

http://code.google.com/apis/ajaxlanguage/
http://github.com/j2labs/goopytrans
"""

import urllib
import simplejson

LANGUAGE_CHOICES = (
    (' ', 'auto_detect'),
    ('af', 'afrikaans'),
    ('sq', 'albanian'),
    ('am', 'amharic'),
    ('ar', 'arabic'),
    ('hy', 'armenian'),
    ('az', 'azerbaijani'),
    ('eu', 'basque'),
    ('be', 'belarusian'),
    ('bn', 'bengali'),
    ('bh', 'bihari'),
    ('bg', 'bulgarian'),
    ('my', 'burmese'),
    ('ca', 'catalan'),
    ('chr', 'cherokee'),
    ('zh', 'chinese'),
    ('zh-cn', 'chinese_simplified'),
    ('zh-tw', 'chinese_traditional'),
    ('hr', 'croatian'),
    ('cs', 'czech'),
    ('da', 'danish'),
    ('dv', 'dhivehi'),
    ('nl', 'dutch'),
    ('en', 'english'),
    ('eo', 'esperanto'),
    ('et', 'estonian'),
    ('tl', 'filipino'),
    ('fi', 'finnish'),
    ('fr', 'french'),
    ('gl', 'galacian'),
    ('ka', 'georgian'),
    ('de', 'german'),
    ('el', 'greek'),
    ('gn', 'guarani'),
    ('gu', 'gujarati'),
    ('iw', 'hebrew'),
    ('hi', 'hindi'),
    ('hu', 'hungarian'),
    ('is', 'icelandic'),
    ('id', 'indonesian'),
    ('iu', 'inuktitut'),
    ('ga', 'irish'),
    ('it', 'italian'),
    ('ja', 'japanese'),
    ('kn', 'kannada'),
    ('kk', 'kazakh'),
    ('km', 'khmer'),
    ('ko', 'korean'),
    ('ku', 'kurdish'),
    ('ky', 'kyrgyz'),
    ('lo', 'laothian'),
    ('lv', 'latvian'),
    ('lt', 'lithuanian'),
    ('mk', 'macedonian'),
    ('ms', 'malay'),
    ('ml', 'malayalam'),
    ('mt', 'maltese'),
    ('mr', 'marathi'),
    ('mn', 'mongolian'),
    ('ne', 'nepali'),
    ('no', 'norwegian'),
    ('or', 'oriya'),
    ('ps', 'pashto'),
    ('fa', 'persian'),
    ('pl', 'polish'),
    ('pt', 'portuguese'),
    ('pa', 'punjabi'),
    ('ro', 'romanian'),
    ('ru', 'russian'),
    ('sa', 'sanskrit'),
    ('sr', 'serbian'),
    ('sd', 'sindhi'),
    ('si', 'sinhalese'),
    ('sk', 'slovak'),
    ('sl', 'slovenian'),
    ('es', 'spanish'),
    ('sw', 'swahili'),
    ('sv', 'swedish'),
    ('tg', 'tajik'),
    ('ta', 'tamil'),
    ('tl', 'tagalog'),
    ('te', 'telugu'),
    ('th', 'thai'),
    ('bo', 'tibetan'),
    ('tr', 'turkish'),
    ('uk', 'ukranian'),
    ('ur', 'urdu'),
    ('uz', 'uzbek'),
    ('ug', 'uighur'),
    ('vi', 'vietnamese'),
    ('cy', 'welsh'),
    ('yi', 'yiddish')
)

def get_abbrev(name):
    """
    Takes a language name and returns abbreviation if found. Returns value error
    on failure.

    Note: ' ' is used for auto_detect
    """
    for lang in LANGUAGE_CHOICES:
        if name == lang[1]:
            return lang[0]
    raise ValueError

def get_long_name(abbrev):
    """
    Takes a language abbreviation and returns long form name. Returns value error
    on failure.

    Note: ' ' is used for auto_detect
    """
    for lang in LANGUAGE_CHOICES:
        if abbrev == lang[0]:
            return lang[1]
    raise ValueError
    
_api_url = "http://ajax.googleapis.com/ajax/services/language/translate"

def _unicode_urlencode(params):
    """
    A unicode aware version of urllib.urlencode. Borrowed from
    pyfacebook :: http://github.com/sciyoshi/pyfacebook/
    """
    if isinstance(params, dict):
        params = params.items()
    return urllib.urlencode([(k, isinstance(v, unicode) and v.encode('utf-8') or v)
                             for k, v in params])

def _run_query(args):
    """
    takes arguments and optional language argument and runs query on server
    """
    url = _api_url
    data = _unicode_urlencode(args)
    search_results = urllib.urlopen(url, data=data)
    json = simplejson.loads(search_results.read())
    return json

def translate(sentences, source='fr', target='en'):
    """
    Takes a list of sentences, source language and target language.
    Returns a list of sentence translations. Places a ValueError in list
    when sentence cannot be translated.
    """
    params = {
        'langpair': '%s|%s' % (source, target),
        'v': '1.0',
    }
    results = list()
    for s in sentences:
        params['q'] = s
        response = _run_query(params)
        if response['responseStatus'] == 200:
            results.append(response['responseData']['translatedText'])
        else:
            results.append(ValueError)
    return results
 
if __name__=='__main__':
    text = raw_input('text :: ')
    language = raw_input('lang :: ')
    sentences = list()
    sentences.append(text)
    translated_text = translate(sentences, source=language, target='en')
    print "\ntranslated :: %s" % (translated_text[0])
    
