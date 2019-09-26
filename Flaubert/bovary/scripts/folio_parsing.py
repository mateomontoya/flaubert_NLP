
# coding: utf-8

# In[3]:


from bs4 import BeautifulSoup
import glob
import re


# Create class with properties for each metadata of the folio.

# In[4]:


class Folio:
    
    def __init__(self, raw):
        self.raw = raw
        self.soup = BeautifulSoup(raw, 'html5lib')
        self.text = self.soup.text
        self.meta = self.soup.find('hors-corpus').text.strip()
        
        try:
            self.chapter = re.search(r'chap\.\s?([0-9])+', self.meta).groups()[0].strip()
        except:
            self.chapter = 'NA'
        
        try:
            self.name = re.search(r'\:(.+?)-', self.meta).groups()[0].strip()
        except:
            self.name = 'NA'
            
        try:
            self.vol = re.search(r'vol\.\s?([0-9]+)', self.meta).groups()[0].strip()
        except:
            self.vol = 'NA'
            
        try:
            self.segment = self.meta.split(',')[0]
        except:
            self.segment = 'NA'
            
        try:
            self.version = re.search(r'\-(.+?),', self.meta).groups()[0].strip()
        except:
            self.version = 'NA'
            
        try:
            self.folio = re.search(r'folio\s?([0-9]+[a-z]?)', self.meta).groups()[0].strip()
        except:
            self.folio = 'NA'
            
    def get_marginalia(self):
        pass


# In[7]:


folios = []

for fpath in glob.glob('folios/*.html')[:20]:
    print(fpath)
    with open(fpath, 'r') as f:
        raw = f.read()
    folios.append(Folio(raw))


# In[8]:


test_soup = folios[2].soup


# In[9]:


body = test_soup('tbody')[1]
rows = body('tr')


# In[10]:


len(rows)


# In[11]:


columns = rows[5]('td')


# In[14]:


for c in columns:
    if 'align' in c.attrs and c['align'] == 'center':
        margin = c
        print(margin)
        print()
        print(margin.text)

