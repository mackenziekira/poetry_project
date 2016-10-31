import requests
import bs4
from random import randint
from time import sleep

url = 'https://www.poetryfoundation.org/poetrymagazine/poems/detail/'
params =  xrange(89513, 89600)

for param in params:

    sleep(randint(10, 100))

    r = requests.get(url + str(param))


    source = bs4.BeautifulSoup(r.text)

    poem = source.select('.poem')

    if not poem:
        continue
    else:
        filename = 'raw_poems/' + str(param) + '.html'
        f = open(filename, 'w')
        f.write(r.text.encode('utf-8'))
        f.close()
