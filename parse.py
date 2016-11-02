import re
from bs4 import BeautifulSoup

class Parse(object):

    regions = {
    "afr":"Africa",
    "ase":"Asia, East",
    "ass":"Asia, South",
    "ast":"Asia, Southeast",
    "aus":"Australia",
    "can":"Canada",
    "car":"Caribbean",
    "ese":"Eastern Europe",
    "eng":"England",
    "fra":"France",
    "ger":"Germany",
    "gre":"Greece",
    "ini":"Ireland & Northern Ireland",
    "isr":"Israel",
    "ita":"Italy",
    "lam":"Latin America",
    "mex":"Mexico",
    "mie":"Middle East",
    "pai":"Pacific Islands",
    "pol":"Poland",
    "rus":"Russia",
    "sca":"Scandinavia",
    "sco":"Scotland",
    "spa":"Spain",
    "usa":"U.S., Mid-Atlantic",
    "usm":"U.S., Midwestern",
    "use":"U.S., New England",
    "usn":"U.S., Northwestern",
    "uss":"U.S., Southern",
    "ust":"U.S., Southwestern",
    "usw":"U.S., Western",
    "wal":"Wales",
    }

    affiliations = {
    "aug":"Augustan",
    "bea":"Beat",
    "bam":"Black Arts Movement",
    "blm":"Black Mountain",
    "con":"Confessional",
    "fug":"Fugitive",
    "geo":"Georgian",
    "har":"Harlem Renaissance",
    "ima":"Imagist",
    "lan":"Language Poetry",
    "mid":"Middle English",
    "mod":"Modern",
    "nys":"New York School",
    "nyt":"New York School (2nd Generation)",
    "obj":"Objectivist",
    "ren":"Renaissance",
    "rom":"Romantic",
    "vic":"Victorian"
    }

    subjects = {
    '': ''
    }

    poetic_terms = {
    '':''
    }

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