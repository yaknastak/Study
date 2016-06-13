import lxml
import re
import csv
import sys
import os
from lxml import etree
from bs4 import BeautifulSoup

def parse_prs(prs):
    """
    на вход берет файл в формате prs, возвращает массив из кортежей, где первый элемент - строка (слово), а второй -- словарь с его характеристиками: (слово, {sentno:_, flex:_, ...})
    """
    flex_gram = '([A-Z0-9_ ]+)([^(syl)0-9]*)(.*)'
    lst = []
    cnt = 0
    prs = open(prs, 'r', encoding = 'utf-8')
    for line in prs:
        if cnt == 0:
            headers= line.split()
        if line[0] != '#':
            cnt = 0
            line = line.split('\t')
            d = {}
            word = line[4]
            if word != ' ':
                for i in range(0, len(line)):
                    d[headers[i][1:]] = line[i]
                fl = re.search(flex_gram, d['gram'])
                try:
                    d['flex'] = fl.group(2).strip()
                    d['gram'] = fl.group(1).strip()
                except: 
                    d['flex'] = ''
                    d['gram'] = ''
                lst.append((word, d))
        cnt += 1
    return(lst)   

def make_xml(data, output):
    """
    конвертирует данные из массива (data), полученного в результате выполнения функции parse_prs, в xml файл
    """
    html = etree.Element("html")
    head = etree.SubElement(html, "head")
    body = etree.SubElement(html, "body")  
    cnt_sent = 0
    cnt_word = 0     
    for item in data:
        if cnt_sent == 0 or item[1]['sentno'] != data[data.index(item) - 1][1]['sentno']:
            se = etree.SubElement(body, "se")
        if cnt_word == 0 or item[1]['wordno'] != data[data.index(item) - 1][1]['wordno']:
            w = etree.SubElement(se, "w")
        ana = etree.SubElement(w, "ana", lex=item[1]['lem'],  morph = item[1]['flex'], gr = item[1]['lex'] + ',' + item[1]['gram'], trans = item[1]['trans']) 
        if cnt_word == len(data) - 1 or item[1]['wordno'] != data[data.index(item) + 1][1]['wordno']:
            ana.tail = item[0] 
        w.tail = item[1]['punctr']
        cnt_word += 1
        cnt_sent += 1
        
    with open(output, "w", encoding="utf-8") as f1:
        f1.write(etree.tostring(html, encoding="utf-8", xml_declaration=True, pretty_print=True).decode("utf-8"))

def make_prs(xml, output):
    """
    конвертирует данные из входного xml файла в файл формата prs
    """
    inp_xml = open(xml, 'r', encoding = 'utf-8')
    soup = BeautifulSoup(inp_xml, 'lxml')
    with open(output, 'w', newline='', encoding = 'utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='\t', quotechar = '"',
                                quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['#sentno'] + ['#wordno'] + ['#lang'] + ['#graph'] + ['#word'] + ['#indexword'] + ['#nvars'] +['#nlems'] + ['#nvar'] + ['#lem'] + ['#trans'] + ['#trans_ru'] + ['#lex'] + ['#gram'] + ['#flex'] + ['#punctl'] + ['#punctr'] + ['#sent_pos'])
        spamwriter.writerow(['#meta.words'] + [len(soup.find_all("w"))])
        spamwriter.writerow(['#meta.sentences'] + [len(soup.find_all("se"))])
        cnt_sent = 1
        for se in soup.find_all("se"):
            cnt_word = 1
            for w in se.find_all("w"):
                word = w.text.strip()
                punctr = w.next_sibling.strip()
                punctl = w.previous_sibling.strip()
                sentno = cnt_sent
                wordno = cnt_word
                lang = ''
                if word[0] != word[0].lower():
                    graph = 'cap'
                else:
                    graph = ''
                nvars = len(w.find_all("ana"))
                lemmas = set()
                for i in range(0, len(w.find_all("ana"))):
                    lemmas.add(w.find_all("ana")[i].get('lex'))
                nlems = len(lemmas)
                cnt_var = 1
                lensen = len(se.find_all("w"))
                if cnt_word == lensen:
                    sent_pos = 'eos'
                elif cnt_word == 1:
                    sent_pos = 'bos'
                else:
                    sent_pos = ''
                for ana in w.find_all("ana"):
                    lem = ana.get('lex')
                    trans = ana.get('trans')
                    flex = ana.get('morph')
                    #разбиваем атрибут gr на две части lex и gram:
                    flex_gram = '([A-Z0-9_ ]+),?(.*)'
                    lex = re.search(flex_gram, ana.get('gr')).group(1)
                    gram = re.search(flex_gram, ana.get('gr')).group(2)
                    nvar = cnt_var
                    spamwriter.writerow([sentno] + [wordno] + [lang] + [graph] + [word] + [''] + [nvars] + [nlems] + [nvar] + [lem] + [trans] + [''] + [lex] + [gram] + [flex] + [punctl] + [punctr] + [sent_pos])
                    cnt_var += 1
                cnt_word += 1            
            cnt_sent += 1
        
def main():
    try:
        direction = sys.argv[1]
        inp = sys.argv[2]
        out = sys.argv[3]
        if not os.path.isfile(inp):
            print('Input file does not exist')
        else:
            if direction == 'prs-xml': 
                make_xml(parse_prs(inp), out)
            elif direction == 'xml-prs':
                make_prs(inp, out)
            else:
                print('Enter: "python xml-prs.py xml-prs inputfile outputfile" or "python xml-prs.py prs-xml inputfile outputfile"')
    except:
        print('Enter: "python xml-prs.py xml-prs inputfile outputfile" or "python xml-prs.py prs-xml inputfile outputfile"')

if __name__ == '__main__':
    main()