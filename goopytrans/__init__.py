#!/usr/bin/env python

"""
Python Interface to Google's translation API.

http://code.google.com/apis/ajaxlanguage/
http://github.com/j2labs/goopytrans
"""

import urllib
import json

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
    
def _unicode_urlencode(params):
    """
    A unicode aware version of urllib.urlencode. Borrowed from
    pyfacebook :: http://github.com/sciyoshi/pyfacebook/
    """
    if isinstance(params, dict):
        params = params.items()
    return urllib.urlencode([(k, isinstance(v, unicode) and v.encode('utf-8') or v)
                             for k, v in params])

def _run_query(url, args=None):
    """
    takes arguments and optional language argument and runs query on server
    """
    print 'URL :: %s' % url
    print 'args :: %s' % args
    if args != None:
        data = _unicode_urlencode(args)
        search_results = urllib.urlopen(url, data=data)
    else:
        search_results = urllib.urlopen(url)
    results = search_results.read()
    json_data = json.loads(results)
    return json_data

def translate(text, source='fr', target='en'):
    """
    Takes some text, source language and target language. Returns
    either the translated text or a ValueError.
    """
    url = "http://ajax.googleapis.com/ajax/services/language/translate"
    params = {
        'langpair': '%s|%s' % (source, target),
        'v': '1.0',
        'q': text,
    }
    response = _run_query(url, params)
    if response['responseStatus'] == 200:
        return response['responseData']['translatedText']
    else:
        raise ValueError

def translate_list(sentences, source='fr', target='en'):
    """
    Takes a list of texts, source language and target language.
    Returns a list of text translations. Places a ValueError in list
    when sentence cannot be translated.
    """
    results = list()
    for s in sentences:
        try:
            response = translate(s, source, target)
            results.append(response)
        except ValueError:
            print 's is not translatable'
            raise
    return results

def detect(text):
    """
    Takes some text and asks Google to detect the language
    Returns a dictionary with 'language', 'isReliable' and 'confidence' keys
    """
    url = 'http://ajax.googleapis.com/ajax/services/language/detect?%s'
    args = _unicode_urlencode({
        'v': '1.0',
        'q': text,
    })
    query_url = url % (args)
    response = _run_query(query_url)
    if response['responseStatus'] == 200:
        return {'isReliable': response['responseData']['isReliable'],
                'confidence': response['responseData']['confidence'],
                'language': response['responseData']['language']}
    else:
        return ValueError
 
if __name__=='__main__':
    text = raw_input('text :: ')
    language = raw_input('\nlang :: ')
    translated_text = translate(text, source=language, target='en')
    print "\ntranslated :: %s" % (translated_text)
    
