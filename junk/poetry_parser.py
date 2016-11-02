from bs4 import BeautifulSoup
import objects
import os

objects = [objects.Author, objects.Title, objects.Poem, objects.AuthorRegion, objects.PoemSubjects, objects.AuthorSchool, objects.PoeticTerms]

raw_poems = os.listdir('raw_poems/')


for f in raw_poems:
    text = open('raw_poems/' + f)

    soup = BeautifulSoup(text, 'html.parser')

    for o in objects:

        data = o.parse_html(soup)
         
        if data:
            d = open('data', 'a')
            d.write(o.name + ': ' + data.encode('utf-8') + '\n')
            d.close()

        else:
            e = open('err', 'a')
            e.write('No ' + o.name + ' found in ' + f + '\n')
            e.close()

    text.close()
