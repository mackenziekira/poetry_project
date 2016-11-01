class AbstractInformation(object):
    """abstract class that other information classes will inherit from"""



class Author(object):
    """an author object"""

    name = 'author'

    @classmethod
    def parse_html(cls, soup):
        selector = soup.find(property="article:author")

        if selector:
            return selector['content']

class Title(object):
    """an author object"""

    name = 'title'

    @classmethod
    def parse_html(cls, soup):
        selector = soup.find('title')

        if selector:
            return selector

