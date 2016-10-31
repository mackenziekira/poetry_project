from bs4 import BeautifulSoup
import model

objects = [model.Author, model.Title]

raw_poems = ['raw_poems/89000.html']


for f in raw_poems:
    text = open(f)

    soup = BeautifulSoup(text)

    for o in objects:

        if type(o.selector) == dict:
            selector = soup.find(**o.selector)
        elif type(o.selector) == str:
            selector = soup.find(o.selector)

        if selector:
            o.data = selector
        else:
            e = open('err', 'a')
            e.write('No ' + o.name + ' found in ' + f + '\n')
            e.close()

    text.close()
