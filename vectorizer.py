from model import Author, Poem, PoemSubject
from model import connect_to_db, db 
from server import app
from sklearn.feature_extraction.text import TfidfVectorizer

connect_to_db(app)

def vectorize_poems(author_id):
    """returns vectorized version of an author's corpus"""
    
    author = Author.query.get(author_id)

    text = []
    for poem in author.poems:
        text.append(poem.body)


    vectorizer = TfidfVectorizer(stop_words='english')

    S = vectorizer.fit_transform(text)

    feature_names = vectorizer.get_feature_names()

    return [S, feature_names]