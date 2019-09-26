from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import codecs
import re
import xlsxwriter
import glob
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

frequencies = {}
# word speechtype entitytype sentiment
wordinfocol = []
wordinforows = []
# sentence syntax, entities sentiment
sentenceinfocol = []
sentenceinforows = []
fullistcol = []
fullistrows = []
seqnum=0

pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
           'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')
entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

# Instantiates a client
client = language.LanguageServiceClient()

def getwordinfo(word):
    

def getsentenceinfo(itemnum, file, sentence):
    text = sentence.rstrip()
    document = types.Document(content=text,type=enums.Document.Type.PLAIN_TEXT,language="fr")
    tokens = client.analyze_syntax(document).tokens
    for token in tokens:
        tokenval = tokenval + token.text.content + " " + pos_tag[token.part_of_speech.tag] + " "
                           
        w.write(token.text.content + " " + pos_tag[token.part_of_speech.tag] + " ")

    entities = client.analyze_entities(document).entities
    for entity in entities:
        entityval = entityval + entity.name + " " + entity_type[entity.type] + " "
        w.write(entity.name + " " + entity_type[entity.type] + " ")

    response = client.analyze_sentiment(document)
    sentiment = response.document_sentiment
    sentenceinfocol = [itemnum, file, sentence, 
    w.write("   Sentiment Score/magnitude: " + str(round(sentiment.score, 2)) + "/" + str(round(sentiment.magnitude, 2)))
    w.write("\r\n")

def text_from_html(file, body):
    soup = BeautifulSoup(body, 'html.parser')
    primary_detail = soup.findAll('i') #gets all items with i tag
    itemnum = 0

    for item in primary_detail:
      if item.text:
        itemnum += 1
        getsentenceinfo(itemnum, file, item.text)
        for word in re.sub("[^\w]", " ",  item.text).split(): #get list of words out of string
            seqnum += 1
            fullistcol = [seqnum, word, file, itemnum]
            fullistrows.append(fullistcol)
            if word in frequencies.keys():
                frequencies[word] += 1
            else:
                frequencies[word] = 1
                getwordinfo(word)


path = 'bovary/folios/*.html'
files = glob.glob(path)

for file in files:
    html = codecs.open(file,'r').read()
    text_from_html(file, html)


workbook = xlsxwriter.Workbook('additions.xlsx')
worksheet = workbook.add_worksheet()
worksheet2 = workbook.add_worksheet()

row = 0
col = 0

for key in frequencies.keys():
    row += 1
    worksheet.write(row, col, key)
    worksheet.write(row, col + 1, frequencies[key])

row=0
col=0
for row in range(len(fullistrows)): 
    fullistcol = fullistrows[row]
    
    worksheet2.write(row, col, fullistcol[0])
    worksheet2.write(row, col+1, fullistcol[1])
    worksheet2.write(row, col+2, fullistcol[2])
    worksheet2.write(row, col+3, fullistcol[3])


workbook.close()

