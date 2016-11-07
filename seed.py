from model import connect_to_db, db 
from model import Poem, Author, Region, Affiliation, Subject, PoemSubject
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
    for r in Parse.regions:
        region = Region(region_name=r)
        db.session.add(region)
        db.session.commit()


def load_affiliations():
    """loads affiliation names and codes"""
    for a in Parse.affiliations:
        affiliation = Affiliation(affiliation_name=a)
        db.session.add(affiliation)
        db.session.commit()



def load_author(soup):
    """loads author from raw_poem file into db"""

    name = Parse.parse_name(soup)


    try:
        Author.query.filter_by(name = name).one()
        return
    except NoResultFound:
        region = Parse.parse_region(soup)
        affiliation = Parse.parse_school(soup)

        try:
            region = Region.query.filter(Region.region_name == region).one().region_id
        except NoResultFound:
            log_err('region', name.encode('unicode-escape'), region)

        try:
            affiliation = Affiliation.query.filter(Affiliation.affiliation_name == affiliation).one().affiliation_id
        except NoResultFound:
            log_err('affiliation', name.encode('unicode-escape'), affiliation)

        author = Author(name=name,
                        region_id=region,
                        affiliation_id=affiliation)
        db.session.add(author)

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




def load_subjects(soup):
    """loads subjects from poem meta tags"""

    subjects = Parse.parse_subjects(soup)

    if subjects:
        for subject in subjects:
            try:
                subject_id = Subject.query.filter(Subject.subject_name == subject).one().subject_id
            except NoResultFound:
                log_err('subject', f, subject)
                s = Subject(subject_name=subject)
                db.session.add(s)
                db.session.commit()
                subject_id = Subject.query.filter(Subject.subject_name == subject).one().subject_id
            

        poem_id = Poem.query.filter(Poem.title == Parse.parse_title(soup)).one().poem_id

        poemsubject = PoemSubject(poem_id=poem_id,
                                    subject_id=subject_id)
        db.session.add(poemsubject)





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
    # load_subjects()

    # Import data into database

    raw_poems = os.listdir('raw_poems/')


    for f in raw_poems:
        text = open('raw_poems/' + f)

        soup = BeautifulSoup(text, 'html.parser')

        
        load_author(soup)
        load_poem(soup)
        load_subjects(soup)
        db.session.commit()

        text.close()


