from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import codecs
import re
import glob
import nltk
#%matplotlib inline

nbsp = u'\xa0'
nb="&nbsp"


w=open("flaubart.txt", "w+")
found=False
foundword=""    
    

def stylometry(txt):
    w.write(txt)
    words = nltk.word_tokenize(txt)

    nopuncwords = ([word for word in words 
                                            if any(c.isalpha() for c in word)])
    word_lengths = [len(word) for word in nopuncwords]
    distributions = nltk.FreqDist(word_lengths)
    distributions.plot(15, title="Flaubart")

           

path = 'roman/*.html'
files = glob.glob(path)
strings = []
for file in files:
    html = codecs.open(file,'r').read()
    soup = BeautifulSoup(html, 'html.parser')
    strings.append(soup.body.text)
stylometry('\n'.join(strings))


w.close()



