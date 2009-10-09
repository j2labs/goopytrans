Goopytrans
=======

Goopytrans is a Python library for interfacing with Google's translation API.


Features
--------

Goopytrans supports translating a single body of text.

    >>> goopytrans.translate('bonjour', source='fr', target='en')
    'hello'

Multiple bodies of text.

    >>> goopytrans.translate_list(('bonjour','merci'), source='fr', target='en')
    ['hello', 'thank you']

And language detection
    >>> goopytrans.detect('bonjour')
    {'isReliable': False, 'confidence': 0.12033016000000001, 'language': 'fr'}


Install
-------

python ./setup.py install


James Dennis <<jd@j2labs.net>>
