#Anastasia Yakovleva

import os
import string
import re

def extract(wiki_file):                                                          
    direct = 'D:/wiki'
    python2 = 'C:/python27/python.exe'
    extractor = direct + "/WikiExtractor.py"
    output = '-o ' + direct
    cmd =  python2 + ' ' + extractor + ' ' + output + ' ' + direct + wiki_file
    os.system(cmd)

def frequent_dic(direct):
    fd = {}
    punctuation = string.punctuation + '—΄¨•“…"*»« ' + '\t'
    for filename in os.listdir(direct):
        f = open(direct + filename, 'r', encoding = 'utf-8')
        for line in f:
            line = line.split()
            for word in line:
                word = word.strip(punctuation)
                word = word.lower()
                if re.search('[a-z<>=0-9а-я]', word) != None:
                    continue
                if re.search('[ἆ-ὦα-ω]', word) == None:
                    continue
                if word not in fd:
                    fd[word] = 1
                else:
                    fd[word] += 1
        f.close()
    concord = open(direct + 'pont_concordance.tsv', 'w', encoding = 'utf-8')
    fdl = []
    for (key, val) in fd.items():
        fdl.append((val, key))
    fdl.sort(reverse = True)
    for item in fdl:
        concord.write(item[1] + '\t' + str(item[0]) + '\n')
    concord.close()
            
    
def main():
    filename = '\pntwiki-20160407-pages-meta-current.xml.bz2'
    dir = 'D:/wiki/AA/'
    extract(filename)
    frequent_dic(dir)
    
if __name__ == '__main__':
    main()


