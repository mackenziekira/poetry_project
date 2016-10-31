class AbstractInformation(object):
    """abstract class that other information classes will inherit from"""



class Author(object):
    """an author object"""

    name = 'author'
    selector = {"property":"article:author"}

class Title(object):
    """an author object"""

    name = 'title'
    selector = 'title'
