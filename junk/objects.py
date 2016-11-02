import re

class AbstractInformation(object):
    """abstract class that other information classes will inherit from"""



class Author(object):
    """an author class"""

    name = 'author'

    @staticmethod
    def parse_html(soup):
        selector = soup.find(property="article:author")

        if selector:
            return selector['content']

class Title(object):
    """a title class"""

    name = 'title'

    @staticmethod
    def parse_html(soup):
        selector = soup.find('title')

        if selector:
            return selector.string

class Poem(object):
    """a poem class"""

    name = 'poem'


    """NOTE TO SELF: IS THIS WORKING??"""

    @staticmethod
    def parse_html(soup):
        selector = soup.find('div', class_="poem")

        if selector:
            return selector.text

class AuthorRegion(object):
    """a author's region"""

    name = 'author_region'

    @staticmethod
    def parse_html(soup):
        selector = soup.find('a', href=re.compile(r"poets#geography"))

        if selector:
            return selector.text

class AuthorSchool(object):
    """a author's school/period"""

    name = 'author_school'

    @staticmethod
    def parse_html(soup):
        selector = soup.find('a', href=re.compile(r"poets#school-period"))

        if selector:
            return selector.text

class PoeticTerms(object):
    """a poem's poetic terms"""

    name = 'poetic_terms'

    @staticmethod
    def parse_html(soup):
        selector = soup.find('a', href=re.compile(r"poets#poetic-terms"))

        if selector:
            return selector.text

class PoemSubjects(object):
    """a poem's subjects"""

    name = 'poem_subjects'

    @staticmethod
    def parse_html(soup):
        selector = soup.find('a', href=re.compile(r"poems#subjects"))

        if selector:
            return selector.text



