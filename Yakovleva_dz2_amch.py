def converter (text, alpha1, alpha2):
    i = len(alpha1) - 1
    while i >= 0:
        text = text.replace(alpha1[i], alpha2[i])
        i -= 1
    return text

f1 = open('alpha_amch.csv', 'r', encoding = 'utf-8')
f2 = open('new', 'w', encoding = 'utf-8')
inp = input("Введите имя файла, содержащего текст на амхарском языке: ")
f3 = open(inp, 'r', encoding = 'utf-8')
voc = []
symbols = []
syllables = []
horizontal = 0
d ={}
lst = []
for line in f1:
    line = line.strip('\n')
    line = line.split('\t')
    for letter in line:
        if horizontal == 0 and letter != line[0]:
            voc.append(letter)
        elif horizontal > 0 and letter == line[0]:
                b = 0
                while b < len(voc):
                    syl = letter + voc[b]
                    d[line[b+1]] = syl
                    b += 1
    horizontal += 1
    
for (key, val) in d.items():
    symbols.append(key)
    syllables.append(val)

for line in f3:
    line = line.lower()
    f2.write(converter(line, symbols, syllables))
f1.close()
f2.close()
f3.close()