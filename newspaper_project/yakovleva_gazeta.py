def dirs (x):
    if os.path.exists(x) == False:
        os.makedirs(x)
    return(None)

import lxml.html
import urllib.request
import os
import os.path
import csv

text = urllib.request.urlopen('http://yaskluch.ru').read().decode()
tree = lxml.html.fromstring(text)
links = []
cnt = 0
i = -1
rdir = 'D:/gazeta'
dir_untagged = rdir + '/untagged_gazeta'
dir_xml = rdir + '/tagged_gazeta_xml'
dir_plaintext = rdir + '/tagged_gazeta'
dirs(rdir)
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
                l = 'http://yaskluch.ru/' + l
            elif l[0] == '/':
                l = 'http://yaskluch.ru' + l
            if l not in links and l[0:18] == 'http://yaskluch.ru':
                links.append(l)
        except:
            continue
    cnt += 1
    i += 1
    if i == len(links) - 1:
        break
art_cnt = 1
with open(rdir + '/' + 'metainf' + '.csv', 'w', newline='', encoding = 'utf-8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';', quotechar = '"',
                            quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['path'] + ['author'] + ['sex'] + ['birthday'] + ['header'] + ['created'] + ['sphere'] + ['genre_fi'] + ['type'] + ['topic'] + ['chronotop'] + ['style'] + ['audience_age'] + ['audience_level'] + ['audience_size'] + ['source'] + ['publication'] + ['publisher'] + ['publ_year'] + ['medium'] + ['country'] + ['region'] + ['language'])
    for link in links:
        text = urllib.request.urlopen(link).read().decode()
        try:
            tree = lxml.html.fromstring(text)
        except:
            print(link)
            continue
        date = tree.xpath('./body/div[@class="wrapper"]/div[@id="center_col"]/ul/li/span[@class="date_start"]/text()')
        texts = tree.xpath(     './body/div[@class="wrapper"]/div[@id="center_col"]/ul/li/span[@class="intro"]/text()')
        header = tree.xpath(     './body/div[@class="wrapper"]/div[@id="center_col"]/ul/li/span[@class="h_2 name"]/h1/text()')
        rubric = tree.xpath('./body/div[@class="wrapper"]/div[@id="center_col"]/ul/li/span[@class="rubrics"]/ul/li/a/text()')
        author = tree.xpath(    './body/div[@class="wrapper"]/div[@id="center_col"]/ul/li/span[@class="author"]/text()')
        if len(date) == 1 and len(texts) == 1:
            for item in date:
                year = item[0:4]
                month = item[5:7]
                new_dir = dir_untagged + '/' + str(year) + '/' + str(month)
                new_xml = dir_xml + '/' + str(year) + '/' + str(month)
                new_plain = dir_plaintext + '/' + str(year) + '/' + str(month)
                dirs(new_dir) 
                dirs(new_xml)
                dirs(new_plain)
                name = new_dir + '/' + 'article' + str(art_cnt) + '.txt'
                name_xml = new_xml + '/' + 'article' + str(art_cnt) + '.txt'
                name_plain = new_plain + '/' + 'article' + str(art_cnt) + '.txt'
                if len(author) == 0:
                    author = 'Noname'
                data = date[0]
                data = data[:-2] + '.' + month + '.' + year
                f = open(name, 'w', encoding = 'utf-8')
                f.write('@au' + ' ' + author + '\n' + '@ti' + ' ' + header[0]     + '\n' + '@da' + ' ' + data + '\n')
                if len(rubric) != 0:
                    f.write('@topic' + ' ' + rubric[0] + '\n' + '@url' + ' ' + link + '\n' + texts[0])
                    spamwriter.writerow([name] + [author] + [' '] + [' '] + [header[0]] + [data] + ['публицистика'] + [' '] + [' '] + [rubric[0]] + [' '] + ['нейтральный'] + ['н-возраст'] + ['н-уровень'] + ['районная'] + [link] + ['Ясный ключ'] + [' '] + [year] + ['газета'] + ['Россия'] + ['Белгородская область'] + ['ru'])
                else:
                    f.write('@url' + ' ' + link + '\n' + texts[0])
                    spamwriter.writerow([name] + [author] + [' '] + [' '] + [header[0]] + [data] + ['публицистика'] + [' '] + [' '] + [' '] + [' '] + ['нейтральный'] + ['н-возраст'] + ['н-уровень'] + ['районная'] + [link] + ['Ясный ключ'] + [' '] + [year] + ['газета'] + ['Россия'] + ['Белгородская область'] + ['ru'])
                f.close()
                fxml = open(name_xml, 'w', encoding = 'utf-8')
                os.system('D:/Python/mystem/mystem.exe -cid --format xml ' + name + ' ' + name_xml)
                fxml.close()
                fplain = open(name_plain, 'w', encoding = 'utf-8')
                os.system('D:/Python/mystem/mystem.exe -cigd --format text ' + name + ' ' + name_plain)
                fplain.close()
                art_cnt += 1
