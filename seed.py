from model import connect_to_db, db 
from model import Poem, Author, Region, Affiliation, PoeticTerm, Subject, PoemPoeticTerm, PoemSubject
from server import app
from bs4 import BeautifulSoup
import os
from parse import Parse
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

def load_regions():
    """loads region names and codes"""
    for k, v in Parse.regions.iteritems():
        region = Region(region_code=k,
                    region_name=v)
        db.session.add(region)
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
        region = Region.query.filter(Region.region_name == region).one().region_code
    except NoResultFound:
        print region
        pass

    try:
        affiliation = Affiliation.query.filter(Affiliation.affiliation_name == affiliation).one().affiliation_code
    except NoResultFound:
        print affiliation
        pass

    try:
        Author.query.filter_by(name = name).one()
        return
    except NoResultFound:
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

    # create all tables
    db.create_all()

    load_regions()
    load_affiliations()

    # Import data into database

    raw_poems = os.listdir('raw_poems/')


    for f in raw_poems:
        text = open('raw_poems/' + f)

        soup = BeautifulSoup(text, 'html.parser')

        load_author(soup)
        load_poem(soup)

        text.close()