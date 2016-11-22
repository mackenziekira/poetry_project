from model import Author, Poem, PoemSubject
from model import connect_to_db, db 
from server import app
from sklearn.feature_extraction.text import TfidfVectorizer

connect_to_db(app)

# love = PoemSubject.query.filter_by(subject_id = 40).all()
# love_poems = []
# for s in love:
#     love_poems.append(s.poem_id)

# nature = PoemSubject.query.filter_by(subject_id = 29).all()
# nature_poems = []
# for s in nature:
#     nature_poems.append(s.poem_id)

# social = PoemSubject.query.filter_by(subject_id = 263).all()
# social_poems = []
# for s in social:
#     social_poems.append(s.poem_id)

# politics = PoemSubject.query.filter_by(subject_id = 16).all()
# politic_poems = []
# for s in social:
#     politic_poems.append(s.poem_id)

# poem_ids = love_poems + social_poems + nature_poems + politic_poems
# poem_ids = set(poem_ids)

# text = []
# for poem in poem_ids:
#     p = Poem.query.get(poem)
#     text.append(p.body)


poems = Poem.query.all()

# author = Author.query.get(323)

text = []
for poem in poems:
    text.append(poem.body)

# f = open('subjectlda', 'r')

# for line in f:
#     text.append(line)

vectorizer = TfidfVectorizer(stop_words='english')

S = vectorizer.fit_transform(text)

feature_names = vectorizer.get_feature_names()