def convert (text, alpha1, alpha2):
    i = len(alpha1) - 1
    while i >= 0:
        text = text.replace(alpha1[i], alpha2[i])
        i -= 1
    return text

f1 =  open('gruz-ssr.txt', 'r', encoding = 'utf-8')
f2 = open('new-gruz.txt', 'w', encoding = 'utf-8')
alph = ['ა', 'ბ', 'გ', 'დ', 'ე', 'ვ', 'ზ', 'ჱ', 'თ', 'ი', 'კ', 'ლ', 'მ', 'ნ', 'ჲ', 'ო', 'პ', 'ჟ', 'რ', 'ს', 'ტ', 'ჳ', 'უ', 'ფ', 'ქ', 'ღ', 'ყ', 'შ', 'ჩ', 'ც', 'ძ', 'წ', 'ჭ', 'ხ', 'ჴ', 'ჯ', 'ჰ', 'ჵ']
ipa = ['ɑ', 'b', 'g', 'd', 'ɛ', 'v', 'z', 'ɛj', 'tʰ', 'ɪ', 'kʼ', 'l', 'm', 'n', 'j', 'ɔ', 'pʼ', 'ʒ', 'r', 's', 'tʼ','wi', 'u', 'pʰ', 'kʰ', 'ɣ', 'qʼ', 'ʃ', 'tʃ', 'ts', 'dz', 'tsʼ', 'tʃʼ','x', 'q', 'dʒ', 'h', 'hɔɛ']

for line in f1:
    line = line.lower()
    f2.write(convert(line, alph, ipa))

f1.close()
f2.close()