from bs4 import BeautifulSoup
import objects

objects = [objects.Author, objects.Title, objects.Poem]

raw_poems = ['raw_poems/89000.html']


for f in raw_poems:
    text = open(f)

    soup = BeautifulSoup(text)

    for o in objects:

        data = o.parse_html(soup)
         
        if data:
            print 'success!', o.name, data

        else:
            e = open('err', 'a')
            e.write('No ' + o.name + ' found in ' + f + '\n')
            e.close()

    text.close()
