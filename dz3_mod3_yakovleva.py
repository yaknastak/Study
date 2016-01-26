import urllib.request
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
        soup = BeautifulSoup(urllib.request.urlopen(l).read())
        name = 'f' + str(cnt)
        f = open(name, 'w', encoding = 'UTF-8')
        f.write(soup.prettify())
        f.close()
    except:
        if l[0] == '?':
            l = 'http://yaskluch.ru/' + l
        elif l[0] == '/':
            l = 'http://yaskluch.ru' + l
        else:
            print(l)
            continue
        soup = BeautifulSoup(urllib.request.urlopen(l).read())
        name = 'f' + str(cnt)
        f = open(name, 'w', encoding = 'UTF-8')
        f.write(soup.prettify())
        f.close()
f1.close()