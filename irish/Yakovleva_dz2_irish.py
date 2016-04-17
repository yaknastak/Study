import re
import string

d = {}
inp = input("Введите имя файла: ")
f1 = open(inp, 'r', encoding = 'utf-8')
f2 = open('heads', 'w', encoding = 'utf-8')
rgexp = '<h3 headword_id="[0-9]+">([a-zA-Z\-\']+)'
rgexp2 = '(.*)</p></div><div class="col-sm-9 result_content">'
for line in f1:
    m = re.search(rgexp, line)
    m2 = re.search(rgexp2, line)
    if m != None:
        val = m.group(1)
    if m2 != None:
        forms = m2.group(1)
        forms = forms.strip()
        forms = forms.split()
        for word in forms:
            word = word.strip(string.punctuation)
            d[word] = val
for (key, val) in d.items():
    f2.write(key + ' ' + val + '\n')
            
f1.close()
f2.close()
