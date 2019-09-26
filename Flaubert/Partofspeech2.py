from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

f=open("favsentences.txt","r")
w=open("partofspeechfav.txt", "w+")
f1 = f.readlines()
pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
           'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')
entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')
row = 0
col = 0
for x in f1:
    client = language.LanguageServiceClient()
    text = x.rstrip()
    document = types.Document(content=text,type=enums.Document.Type.PLAIN_TEXT,language="fr")
    tokens = client.analyze_syntax(document).tokens
    w.write(text + "    Part of Speech Tag: ")
    for token in tokens:
        w.write(token.text.content + " " + pos_tag[token.part_of_speech.tag] + " ")

    entities = client.analyze_entities(document).entities
    w.write("   Entity Type: ")
    for entity in entities:
        w.write(entity.name + " " + entity_type[entity.type] + " ")

    response = client.analyze_sentiment(document)
    sentiment = response.document_sentiment
    w.write("   Sentiment Score/magnitude: " + str(round(sentiment.score, 2)) + "/" + str(round(sentiment.magnitude, 2)))
    w.write("\r\n")

w.close()
f.close()
