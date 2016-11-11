NEED TO RUN
pip install -U spacy
python -m spacy.en.download all


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



 |          from spacy.en import English
 |          nlp = English()
 |          tokens = nlp(u'Mr. Best flew to New York on Saturday morning.')
 |          ents = list(tokens.ents)
 |          assert ents[0].label == 346
 |          assert ents[0].label_ == 'PERSON'
 |          assert ents[0].orth_ == 'Best'
 |          assert ents[0].text == 'Mr. Best'
