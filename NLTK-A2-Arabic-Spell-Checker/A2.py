# -*- coding: utf8 -*-
import re, collections, nltk
import codecs
import time
start_time = time.time()

def words(text): return re.findall(ur'[\u0621-\u063A\u0640-\u065E]+', text)

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

tmp1 = re.compile(ur'[\u064B-\u065F\u0640]+',re.UNICODE)

#NWORDS = train(tmp1.sub('',words(file(ur'quran-uthmani.txt').read())))


#print words(file(ur'quran-uthmani.txt').read())

with codecs.open('arabic.txt','r',encoding='utf-8') as f:
    
    NWORDS=train(tmp1.sub('',word2) for word2 in words(f.read()))



alphabet = u'\u0621\u0622\u0623\u0624\u0625\u0626\u0627\u0628\u0629\u062a\u062b\u062c\u062d\u062e\u062f\u0630\u0631\u0632\u0633\u0634\u0635\u0636\u0637\u0638\u0639\u063a\u0640\u0641\u0642\u0643\u0644\u0645\u0646\u0647\u0648\u0649\u064a'

def edits1(word):
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts    = [a + c + b     for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)


def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)



'''---------------- write the word here
                \ |
                \ |
                \ V
'''
ed2 = correct(u"هيام")

print "--------------------------------------"



print repr(ed2).decode("unicode-escape")


print ed2


print "--------------- exeution time in about 1440336 terms -----------------------"


print("--- %s seconds ---" % (time.time() - start_time))
