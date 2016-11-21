from model import Author, Poem
from model import connect_to_db, db 
from server import app
from sklearn.feature_extraction.text import TfidfVectorizer

# connect_to_db(app)

# poems = Poem.query.all()

# author = Author.query.get(1)
text = []

# for poem in poems:
#     text.append(poem.body)

f = open('mashup.txt', 'r')

for line in f:
    text.append(line)

vectorizer = TfidfVectorizer(stop_words='english')

S = vectorizer.fit_transform(text)

feature_names = vectorizer.get_feature_names()