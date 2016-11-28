from model import connect_to_db, db 
from model import Poem, Author, Region, Affiliation, Subject, PoemSubject
from sqlalchemy import func

def get_headlines(term):
    """get relevant lines that contain the search term"""

    qry = 'SELECT *, ts_headline(body, q) AS headline FROM poems, to_tsquery(\'{}\') q WHERE q @@ tsv'.format(term)
    cursor = db.session.execute(qry)
    headlines = cursor.fetchall()
    db.session.commit()
    return headlines

def get_subjects(headlines):
    """get relevant subjects associated with poems returned from search term"""

    poem_ids = [0]

    for poem in headlines:
        poem_ids.append(poem[0])

    poem_ids = tuple(poem_ids)

    qry = "select s.subject_name, count(s.subject_name) from poems_subjects as ps join subjects as s on ps.subject_id = s.subject_id where ps.poem_id in {} group by s.subject_name order by count(s.subject_name) desc limit 5".format(poem_ids)

    cursor = db.session.execute(qry)

    subjects = cursor.fetchall()

    db.session.commit()
    return subjects

def get_authors():
    """retrieve list of author objects (sorted by word stats) from the cache. else calculate list and return"""
    
    authors = Author.query.all()

    for author in authors:
        qry = 'SELECT count(*) FROM ts_stat(\'SELECT tsv FROM poems WHERE author_id = {}\');'.format(author.author_id)

        cursor = db.session.execute(qry)

        word_count = cursor.fetchone()

        # divide by /len(author.poems) to attenuate mismatch in sample size?
        author.word_count = int(word_count[0])
        db.session.expunge(author)

        db.session.commit()

    authors = sorted(authors, key=lambda author: author.word_count, reverse=True)
        
    return authors

def author_top_words(author_id):
    """returns list of top words for a particular author"""

    qry = 'SELECT * FROM ts_stat(\'SELECT tsv FROM poems WHERE author_id = {}\') ORDER BY nentry DESC, ndoc DESC, word;'.format(author_id)

    cursor = db.session.execute(qry)

    words = cursor.fetchall()

    db.session.commit()

    author = Author.query.options(db.joinedload('poems')).get(author_id)

    author.top_words = words

    return author

def subject_top_words(subject_id):
    """returns dictionary of top words for a particular subject"""

    # better way to fix this? need tuple to have at least two values, so this ensures no errors are thrown by psycopg2 
    poem_ids = [0, 0]

    relevant_poems = PoemSubject.query.filter_by(subject_id=subject_id).all()

    for poem in relevant_poems:
        poem_ids.append(poem.poem_id) 
    print poem_ids   

    poem_ids = tuple(poem_ids)


    qry = 'SELECT * FROM ts_stat(\'SELECT tsv FROM poems WHERE poem_id IN {}\') ORDER BY nentry DESC, ndoc DESC, word LIMIT 10;'.format(poem_ids)


    cursor = db.session.execute(qry)

    words = cursor.fetchall()

    db.session.commit()

    word_dict = []

    for row in words:
        word_dict.append({'word': row[0], 'count': row[2]})

    return word_dict
