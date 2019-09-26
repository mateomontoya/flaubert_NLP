from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import codecs
import re
import glob
import nltk

nbsp = u'\xa0'
nb="&nbsp"

f=open("favwordsprofnadaff.txt","r")
f1 = f.readlines()
w=open("madamebovariautoselectsentences.txt", "w+")
found=False
foundword=""
    

def text_from_html(file, body):
    soup = BeautifulSoup(body, 'html.parser')
    sents = nltk.sent_tokenize(soup.body.text)
    for x in f1:
        result = [sent for sent in sents if x.strip() in sent]
        w.write("############################# " + x.strip() + "#########################")
        w.write("\r\n")
        for s in result:
            w.write(s)
            w.write("\r\n")
           

path = 'bovary/folios/*.html'
files = glob.glob(path)

for file in files:
    html = codecs.open(file,'r').read()
    text_from_html(file, html)


w.close()
f.close()


