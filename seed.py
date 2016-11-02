from model import connect_to_db, db 
from model import Poem, Author, Region, Affiliation, PoeticTerm, Subject, PoemPoeticTerm, PoemSubject
from server import app
from bs4 import BeautifulSoup
import os
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

def load_author(soup):
    """loads author from raw_poem file into db"""

    name = Author.parse_name(soup)

    try:
        Author.query.filter_by(name = name).one()
        return
    except NoResultFound:
        author = Author(name=name)
        db.session.add(author)
        db.session.commit()
    except MultipleResultsFound:
        print 'multiple results found for author name. db corrupted. investigate!'

def load_poem(soup):
    """load poem from raw_poem file into database"""

    title = Poem.parse_title(soup)
    body = Poem.parse_poem(soup)
    author_id = Author.query.filter(Author.name == Author.parse_name(soup)).one().author_id
    

    poem = Poem(title=title,
        body=body,
        poem_url="",
        author_id=author_id)

    db.session.add(poem)

    db.session.commit()




if __name__ == "__main__":
    connect_to_db(app)

    # drop all tables
    db.drop_all()

    # create all tables
    db.create_all()

    # Import data into database

    raw_poems = os.listdir('raw_poems/')


    for f in raw_poems:
        text = open('raw_poems/' + f)

        soup = BeautifulSoup(text, 'html.parser')

        load_author(soup)
        load_poem(soup)

        text.close()