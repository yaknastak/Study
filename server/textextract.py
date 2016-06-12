import lxml.html
import urllib.request
import os
import re

def collect_links(url):
    text = urllib.request.urlopen(url).read().decode()
    tree = lxml.html.fromstring(text)
    links = []
    cnt = 0
    i = -1
    while True:
        if cnt >= 1:
            try:
                text = urllib.request.urlopen(links[i]).read().decode()
                tree = lxml.html.fromstring(text)
            except:
                i+= 1
                continue
        for link in tree.iter('a'):  
            l = link.get('href')
            try:
                if l[0] == '?':
                    l = url + '/' + l
                elif l[0] == '/':
                    l = url + l
                if l not in links and re.match(url, l) != None:
                    links.append(l)
            except:
                continue
        cnt += 1
        i += 1
        if i == len(links) - 1:
            break
    return(links)

links = collect_links('http://yaskluch.ru')
art_cnt = 1
for link in links:
    text = urllib.request.urlopen(link).read().decode()
    try:
        tree = lxml.html.fromstring(text)
    except:
        print(link)
        continue
    texts = tree.xpath(     './body/div[@class="wrapper"]/div[@id="center_col"]/ul/li/span[@class="intro"]/text()')
    if len(texts) > 0:
        f = open(str(art_cnt), 'w', encoding = 'utf-8')
        for t in texts:
            f.write(t)
        f.close()
        art_cnt += 1
    if art_cnt > 3:
        break
