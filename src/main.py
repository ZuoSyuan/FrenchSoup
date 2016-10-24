# -*- coding: UTF-8 -*-
import codecs
import urllib2
from bs4 import BeautifulSoup


SPECIAL_SIGN = u'’'
DE_QUOTE = lambda s: s[1:-1] 
QUOTE = lambda s: u"[%s]" % s

import re, urlparse
def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

def iriToUri(iri):
    parts= urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti==1 else urlEncodeNonAscii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
    )

def getPhonitic(word):
    try:
        url = u"http://www.frdic.com/dicts/fr/%s" % (word)
        #print iriToUri(url)
        data = urllib2.urlopen(iriToUri(url))
        soup = BeautifulSoup(data, "html.parser")
        # <span class="Phonitic">[de]</span>
        PhoniticDOM = soup.find("span", {'class': 'Phonitic'})
        if PhoniticDOM is None:
            raise Exception, 'Phonitic Not Found'
    except Exception, e:
        #print e
        return '!!!ERR!!!'
        
    return PhoniticDOM.string

def memoWrapper(wrappedFunc):
    _cache = {}
    def wrapper(*args):
        if args not in _cache:
            _cache[args] = wrappedFunc(*args)
        return _cache[args]
    return wrapper

@memoWrapper
def transferWord(word):
    if -1 != word.find(SPECIAL_SIGN):
        ind = word.index(SPECIAL_SIGN)
        remPrefix = word[ind-1]
        inWord = word[ind+1:]
        ret = DE_QUOTE(getPhonitic(inWord))
        ret = remPrefix + ret
    elif u'les' == word:
        ret = u'le'
    else:
        ret = DE_QUOTE(getPhonitic(word))
    
    return ret

def transferWords(words):
    phonitics = map(transferWord, words)
    return phonitics

if __name__ == '__main__':
    
    lines = []
    with codecs.open(r'./docs/input.txt', 'r', encoding='utf-8') as f:
        line = f.readline().decode('utf8')
        while line:
            if line.startswith(u'#') or line.startswith(u'\n') or line.startswith(u'\r\n'):
                pass
            elif unicode(line):
                lines.append(unicode(line))
            line = f.readline()
                  
    # remove Chinese part
    stripLast = lambda s: s.split(u' ')[:-1]
    remindLast = lambda s: s.split(u' ')[-1]
    reminds = map(remindLast, lines)
    lines = map(stripLast, lines)
    
    retWords = []
    for words in lines:
        ret = transferWords(words)
        print ret
        retWords.append(QUOTE(' '.join(ret)))
    
    retLines = [p1 + u' ' + p2 for p1, p2 in zip(retWords, reminds)]
    lines = map(' '.join, lines)
    retLines = [p1 + u' ' + p2 for p1, p2 in zip(lines, retLines)]
    
    with codecs.open(r'./docs/output.txt', 'w', encoding='utf-8') as f:
        for lines in retLines:
            f.write(lines)
        
    #===========================================================================
    # word = u'd’orange'
    # ret = transferWord(word)
    # print ret
    #===========================================================================
    
    