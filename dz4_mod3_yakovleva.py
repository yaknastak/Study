import lxml.html
import urllib.request
import csv
from bs4 import BeautifulSoup

cnt = 0
f1 = open('f0', 'w', encoding = 'UTF-8')
html = urllib.request.urlopen('http://yaskluch.ru').read()
soup = BeautifulSoup(html)
f1.write(soup.prettify())
for link in soup.find_all('a'):
    l = link.get('href')
    cnt += 1
    try:
        text = urllib.request.urlopen(l).read().decode()
        print(l)
        tree = lxml.html.fromstring(text) 
        date = tree.xpath('.//span[@class="intro"]/text()')
        name = 'f' + str(cnt)
        f = open(name, 'w', encoding = 'UTF-8')
        for item in date:
            f.write(item + '\n')
        f.close()
    except:
        if l[0] == '?':
            l = 'http://yaskluch.ru/' + l
        elif l[0:1] == '/?':
            l = 'http://yaskluch.ru' + l
        else:
            print(l)
            continue
        text = urllib.request.urlopen(l).read().decode()
        print(l)
        tree = lxml.html.fromstring(text)
        date = tree.xpath('.//span[@class="intro"]/text()')
        name = 'f' + str(cnt)
        f = open(name, 'w', encoding = 'UTF-8')
        for item in date:
            f.write(item + '\n')
        f.close()
f1.close()


