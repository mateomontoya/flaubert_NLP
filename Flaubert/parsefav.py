from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import codecs
import re
import glob
import nltk

nbsp = u'\xa0'
nb="&nbsp"

f=open("fav.txt","r")
f1 = f.readlines()
w=open("favsent.txt", "w+")
found=False
foundword=""
    

def text_from_html(file, body):
    soup = BeautifulSoup(body, 'html.parser')
    sents = nltk.sent_tokenize(soup.text)
    for sent in sents:
        w.write(sent)
        w.write("\r\n")
    w.write("#############################")
    result = [sent for sent in sents if "bien" in sent]
    w.write("\r\n")
    for s in result:
        w.write(s)
        w.write("\r\n")
    w.write("#############################")

    soup.prettify(formatter=lambda s: s.replace(u'\xa0', ' '))
    #soup = soup.replace(nbsp, '')
    primary_detail = soup.findAll('a') #gets all items with i tag
    #primary_detail = primary_detail.replace(nonBreakSpace, '')
    itemnum = 0

    for item in primary_detail:
      if item.text:
        sentence=item.text
        sentence.strip()
        sentence = sentence.replace("&nbsp;", "")
        " ".join(sentence.split())
        found=False
        for word in re.sub("[^\w]", " ",  sentence).split(): #get list of words out of string
            if found:
                break;
            for x in f1:
                if x.strip() == word:
                    foundword=word
                    found=True
                    break                
        if found:
            w.write("======" + foundword+"========")
            w.write("\r\n")
            w.write(sentence)
            w.write("\r\n")
            

path = 'bovary/roman/roman_visuep_rep_001.html'
files = glob.glob(path)

for file in files:
    html = codecs.open(file,'r').read()
    text_from_html(file, html)


w.close()
f.close()


