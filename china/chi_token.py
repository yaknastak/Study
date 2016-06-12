import re
import string
import lxml
from lxml import etree
from bs4 import BeautifulSoup

def make_dict(chinese_dic):
    """
    парсит китайский словарь. На вход - файл, на выходе словарь {слово:{транскрипция: транскрипция, значение: значение}} 
    """
    cnt = 0
    chinaDict = open(chinese_dic, 'r', encoding = 'utf-8')
    d ={}
    for line in chinaDict:
        line = line.strip()
        if line[0] != '#':
            l = line.split('/')
            d1 = {}
            word = l[0]
            transcr = re.search('\[(.*?)\]', word)
            sem = re.search ('\]\s/(.+)', line)
            if transcr != None and sem != None:
                word = word[:word.index('[')]
                w = word.split()
                new_orth = w[1]
                transcr = transcr.group(1)
                sem = sem.group(1)
                d1['transcr'] = transcr
                d1['sem'] = sem
                d[new_orth] = d1
            else:
                continue
    chinaDict.close()
    return(d)

def make_sent(chinese_sent):
    """
    берет на вход файл xml с китайскими предложениями, удаляет пунктуацию и возрвращает массив с предложениями.  
    """
    punct = string.punctuation + '“！”？。：…，'
    chinaSent = open(chinese_sent, 'r', encoding = 'utf-8') 
    soup = BeautifulSoup(chinaSent, "lxml")
    sent = soup.find_all("se")  
    LstSent = []
    for item in sent:
        LstSent.append(item.get_text().strip(punct))
    chinaSent.close()
    return(LstSent)

def make_xml(d, sents):    
    """
    создает xml файл с разметкой китайских токенов. d - китайский словарь, sents -массив предложений. 
    """
    punct = string.punctuation + '“！”？。：…，'
    lst = []  
    html = etree.Element("html")
    head = etree.SubElement(html, "head")
    body = etree.SubElement(html, "body")
    for sent in sents:
        sent = sent.strip(punct)
        new_sent = re.sub('[“！”？。：…]', '', sent)
        se = etree.SubElement(body, "se")
        maxlen = len(sent)
        while maxlen > 0:
            current = new_sent[0:maxlen]
            if current in d:
                lst.append((current, d[current]))
                w = etree.SubElement(se, "w")
                ana = etree.SubElement(w, "ana", lex=current,transcr=d[current]['transcr'], sem=d[current]['sem'])
                ana.tail = current
                new_sent = new_sent[maxlen:]
                maxlen = len(new_sent)
                continue
            else:
                maxlen -= 1
    with open("output.xml", "w", encoding="utf-8") as f1:
        f1.write(etree.tostring(html, encoding="utf-8", xml_declaration=True, pretty_print=True).decode("utf-8"))
        
def main():
    chinaDict = make_dict('cedict_ts.u8')
    sent = make_sent('stal.xml')
    make_xml(chinaDict, sent)
    
if __name__ == '__main__':
    main()
