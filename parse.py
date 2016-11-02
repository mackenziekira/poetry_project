import re
from bs4 import BeautifulSoup

class Parse(object):

    regions = ['Africa','Asia, East','Asia, South','Asia, Southeast','Australia','Canada','Caribbean','Eastern Europe','England','France','Germany','Greece','Ireland & Northern Ireland','Israel','Italy','Latin America','Mexico','Middle East','Pacific Islands','Poland','Russia','Scandinavia','Scotland','Spain','U.S., Mid-Atlantic','U.S., Midwestern','U.S., New England','U.S., Northwestern','U.S., Southern','U.S., Southwestern','U.S., Western','Wales']

    affiliations = ['Augustan','Beat','Black Arts Movement','Black Mountain','Confessional','Fugitive','Georgian','Harlem Renaissance','Imagist','Language Poetry','Middle English','Modern','New York School','New York School (2nd Generation)','Objectivist','Renaissance','Romantic','Victorian']

    subjects = ['Love','Nature','Social Commentaries','Religion','Living','Relationships','Activities','Arts & Sciences','Mythology & Folklore']

    poetic_terms = ['Ballad','Haiku','Limerick','Sestina','Sonnet','Villanelle','Pantoum','Ghazal','Couplet','Ottava Rima','Terza Rima','Rhymed Stanza','Mixed','Tercet','Quatrain','Free Verse','Blank Verse','Syllabic','Common Measure','Epigraph','Assonance','Consonance','Alliteration','Allusion','Simile','Metaphor','Imagery','Refrain','Aphorism','Persona','Imagist','Confessional','Symbolist','Ode','Pastoral','Aubade','Dramatic Monologue','Elegy','Epistle','Epithalamion','Concrete or Pattern Poetry','Epigram','Prose Poem','Series/Sequence','Visual Poetry','Ars Poetica','Ekphrasis','Epic','Nursery Rhymes']

    @staticmethod
    def parse_name(soup):
        selector = soup.find(property="article:author")

        if selector:
            return selector['content']

    @staticmethod
    def parse_region(soup):
        selector = soup.find('a', href=re.compile(r"poets#geography"))

        if selector:
            return selector.text

    @staticmethod
    def parse_school(soup):
        selector = soup.find('a', href=re.compile(r"poets#school-period"))

        if selector:
            return selector.text

    @staticmethod
    def parse_title(soup):
        selector = soup.find('title')

        if selector:
            return selector.string

    @staticmethod
    def parse_poem(soup):
        selector = soup.find('div', class_="poem")

        if selector:
            return selector.text