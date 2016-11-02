from model import connect_to_db, db 
from model import Poem, Author, Region, Affiliation, PoeticTerm, Subject, PoemPoeticTerm, PoemSubject
from server import app
from bs4 import BeautifulSoup
import os
from parse import Parse
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

def log_err(category, associated_thing, value):
    """logs errors in db population process"""

    e = open('err', 'a')
    e.write(category + ' for ' + associated_thing + ' was ' + str(value) + '\n')
    e.close()


def load_regions():
    """loads region names and codes"""
    for k, v in Parse.regions.iteritems():
        region = Region(region_code=k,
                    region_name=v)
        db.session.add(region)
        db.session.commit()

def load_subjects():
    """loads subject names and codes"""
    for k, v in Parse.subjects.iteritems():
        subject = Subject(subject_code=k,
                    subject_name=v)
        db.session.add(subject)
        db.session.commit()

def load_poeticterms():
    """loads poetic terms and codes"""
    for term in Parse.poetic_terms:
        term = PoeticTerm(term_name=term)
        db.session.add(term)
        db.session.commit()


def load_affiliations():
    """loads affiliation names and codes"""
    for k, v in Parse.affiliations.iteritems():
        affiliation = Affiliation(affiliation_code=k,
                            affiliation_name=v)
        db.session.add(affiliation)
        db.session.commit()


def load_author(soup):
    """loads author from raw_poem file into db"""

    name = Parse.parse_name(soup)
    region = Parse.parse_region(soup)
    affiliation = Parse.parse_school(soup)

    try:
        Author.query.filter_by(name = name).one()
        return
    except NoResultFound:

        try:
            region = Region.query.filter(Region.region_name == region).one().region_code
        except NoResultFound:
            log_err('region', name.encode('unicode-escape'), region)

        try:
            affiliation = Affiliation.query.filter(Affiliation.affiliation_name == affiliation).one().affiliation_code
        except NoResultFound:
            log_err('affiliation', name.encode('unicode-escape'), affiliation)

        author = Author(name=name,
                        region_code=region,
                        affiliation_code=affiliation)
        db.session.add(author)
        db.session.commit()
    except MultipleResultsFound:
        print 'multiple results found for author name. db corrupted. investigate!'




def load_poem(soup):
    """load poem from raw_poem file into database"""

    title = Parse.parse_title(soup)
    body = Parse.parse_poem(soup)
    author_id = Author.query.filter(Author.name == Parse.parse_name(soup)).one().author_id
    

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

    # clear the error logging file
    e = open('err', 'w')
    e.close()

    # create all tables
    db.create_all()

    load_regions()
    load_affiliations()
    load_subjects()
    load_poeticterms()

    # Import data into database

    raw_poems = os.listdir('raw_poems/')


    for f in raw_poems:
        text = open('raw_poems/' + f)

        soup = BeautifulSoup(text, 'html.parser')

        load_author(soup)
        load_poem(soup)

        text.close()