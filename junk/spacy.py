import spacy
from model import connect_to_db, db 
from model import Poem, Author, Region, Affiliation, Subject, PoemSubject

nlp = spacy.load('en')

poems = Poem.query.all()

docs = [nlp(body) for body in [poem.body for poem in poems]]

t = nlp.vocab[u'kiss']

sents = []
objects = []

for doc in docs:
    for sent in doc.sents:
        for token in sent:
            if token.orth == t.orth:
                sents.append(sent.text)
                objects.append(poems[docs.index(doc)])

