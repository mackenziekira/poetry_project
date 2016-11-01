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


    """NOTE TO SELF: IS THIS WORKING??"""

    @staticmethod
    def parse_html(soup):
        selector = soup.find('a', href=re.compile(r"poets#geography"))
        print selector.text

        # selector = soup.find(text="Poet's Region").parent.parent.parent
        # print selector.text


        if selector:
            return selector.text

