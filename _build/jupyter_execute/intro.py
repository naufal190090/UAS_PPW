#!/usr/bin/env python
# coding: utf-8

# # Crawling Web

# ### Crwaling Web Adalah

# Jadi crawling web adalah sebuah proses dimana kita akan mengambil sebuah data dari sebuah web menggunakan code. Untuk crawling web saya menggunakan file python biasa yang harus menggunakan visual studio code, berikut ini adalah code nya:

# In[1]:


import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        x = 100000
        for i in range (1,500):
            x +=1
            urls = [
                'https://pta.trunojoyo.ac.id/welcome/detail/070411'+str(x),
                'https://pta.trunojoyo.ac.id/welcome/detail/040411'+str(x),
            ]
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield{
            'judul':response.css('#content_journal > ul > li > div:nth-child(2) > a::text').extract(),
            'Penulis':response.css('#content_journal > ul > li > div:nth-child(2) > div:nth-child(2) > span::text').extract(),
            'Pembimbing 1':response.css('#content_journal > ul > li > div:nth-child(2) > div:nth-child(3) > span::text').extract(),
            'Pembimbing 2':response.css('#content_journal > ul > li > div:nth-child(2) > div:nth-child(4) > span::text').extract(),
            'Abstrak':response.css('#content_journal > ul > li > div:nth-child(4) > div:nth-child(2) > p::text').extract(),
            'Abstract':response.css('#content_journal > ul > li > div:nth-child(4) > div:nth-child(4) > p::text').extract()
        }
        


# sebelum menjalankan code diatas harus menginstal terlebih dahulu framework scrapy dengan cara
# buka cmd menggunakan run as administrator
# setelah itu ketikkan

# In[2]:


pip install scrapy


# ### Melakukan Crawling Web

# untuk menjalankannya pertama harus di save terlebih dahulu code diatas didalam file berformat py. setelah itu buka menggunakan visual studio code dengan cara open folder dimana file tersebut disimpan bukan open file tersebut. setelah folder tempat file crawling itu dibuka tinggal buka file nya setelah itu buka terminal dan ketikkan

# In[3]:


scrapy runspider nama_file.py -o data_awal_crawling.csv


# hasil dari save code diatas akan menghasilkan file berformat csv dimana akan ada banyak kolom kosong yang ada
# oleh karena itu maka diperlukan sedikit modifikasi untuk menghapus kolom yang kosong dan sekaligus mengubah file dari csv ke xlsx
# berikut ini kodenya

# ## Menghilangkan Kolom Kosong

# In[3]:


import pandas as pd
data = pd.read_csv('data_awal_crawling.csv')


# code diatas digunakan untuk mengimportkan library pandas yang akan digunakan untuk code selanjutnya. Lalu baris kedua digunakan untuk membaca file yang sudah di crawling.

# In[4]:


data.dropna(inplace=True)
data.isnull().sum()


# pada code di atas baris pertama digunakan untuk menghapus baris kosong, lalu baris kedua digunakan untuk medeteksi missing value kemudian dijumlahkan. setelah itu hasilnya di save dalam format xlsx dengan menggunakan code dibawah ini.

# In[5]:


data.to_excel("hasil_crawling.xlsx")


# ## Latent Semantic Analysis (LSA)

# Latent Semantic Analysis adalah suatu algoritma yang dapat digunakan untuk melakukan analisis pada frase/kalimat dalam sekumpulan dokumen, analisis yang dilakukan adalah menganalisa apakah setiap frase/kalimat memiliki hubungan antara lain atau tidak.Pada proses LSA akan menggunakan Singularity Value Decomposition (SVD atau dekomposisi nilai tunggal untuk mengambil informasi dan melakukan pengklasifikasian. kali ini yang dicari adalah hubungan setiap topik yang ada pada data hasil ceawling web yang sudah di lakukan preprocessing. berikut ini adalah langkah langkah nya

# ## Text Processing

# Langkah ini sangat dibutuhkan dikarenakan data awal tersebut masih tidak teratur jadi akan diolah agar siap untuk diproses pada langkah selanjutnya. berikut ini adalah langkah langkah dari preprocessing

# ## Import Modules

# In[6]:


# data visualisation and manipulation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns
from openpyxl import load_workbook #library untuk menampilkan dokumen
#configure
#import nltk
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize

#preprocessing
from nltk.corpus import stopwords  #stopwords
from nltk import word_tokenize,sent_tokenize # tokenizing
from nltk.stem import PorterStemmer,LancasterStemmer  # using the Porter Stemmer and Lancaster Stemmer and others
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer  # lammatizer from WordNet

# for named entity recognition (NER)
from nltk import ne_chunk

# vectorizers for creating the document-term-matrix (DTM)
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer

#stop-words
stop_words=set(nltk.corpus.stopwords.words('english'))


# Code diatas digunakan untuk mengimport berbagai library yang akan digunakan pada code selanjutnya. 

# ## Loading Dataset

# In[7]:


wr = load_workbook(filename = 'hasil_crawling.xlsx')
sheet_range = wr['Sheet1']

data = pd.DataFrame(sheet_range.values)
data.columns = ['','judul','Penulis', 'Pembimbing 1','Pembimbing 2', 'Abstrak', 'Abstract']


# code diatas digunakan untuk membaca file yang bernama "hasil_crawling.xlsx". setelah itu pada baris ke 2 digunakan untuk mengambil hanya pada sheet 1 yang ada pada file excel. lalu langkah selanjutnya adalah untuk mengambil kolom pada baris pertama dengan nama yang sudah tertera pada baris ke 5.

# In[8]:


data.head()


# code diatas digunakan untuk menampilkan hasil dari file yang sudah dibaca pada code sebelumnya.

# In[11]:


df = data[['Abstrak']]
df.head()


# setelah itu membuat variabel yang hanya berisi kolom dari Abstrak.

# ## Data Cleaning dan Preprocessing Teks

# pada langkah ini digunakan untuk menghilangkan kata tambahan yaitu kata yang karakternya kurang dari 3 angka.

# In[12]:


def clean_text(headline):
  le=WordNetLemmatizer()
  word_tokens=word_tokenize(headline)
  tokens=[le.lemmatize(w) for w in word_tokens if w not in stop_words and len(w)>3]
  cleaned_text=" ".join(tokens)
  return cleaned_text
  
  


# pada code disini adalah membuat sebuah fungsi yang berfungsi untuk melakukan data cleaning.

# In[13]:


df_bersih = df['Abstrak'].apply(clean_text)
df_bersih.head()
df.head()


# disini dapat terlihat perbedaan dari kata sebelum dilakukan preprocessing dan sesudah dimana kata ada dihilangkan.

# In[14]:


df = df_bersih
df.head()


# setelah itu jadikan df_bersih sebagai df lalu ditampilkan

# ## Melakukan Ekstraksi Fitur dan Membuat Dokumen term Matrix

# dokumen term matrix atau disingkan DTM adalah representasi dari dokumen dalam corpus. DTM akan mempresentasikan dokumen dalam struktur numerik. melalui DTM kita dapat melakukan analisis yang lebih menarik.

# In[15]:


vect =TfidfVectorizer(stop_words=stop_words,max_features=1000) # to play with. min_df,max_df,max_features etc...
vect_text=vect.fit_transform(df)
print(vect_text.shape)
print(vect_text)


# dengan menggunakan code diatas kita dapat melihat kata kata yang paling sering keluar dan juga kata kata yang jarang keluar dengan cara memperhatikan seberapa besar skor idf. semakin kecil nilai dari skor idf berarti semakin sering muncul kata tersebut.

# In[20]:


idf=vect.idf_
dd=dict(zip(vect.get_feature_names_out(), idf))
l=sorted(dd, key=(dd).get)
# print(l)
print(l[0],l[-1])
print(dd['gerak'])
print(dd['hidup'])


# code di atas digunakan untuk melakukan extraksi fitur dari vectorizer. lalu pada 2 baris terbawah digunakan untuk menampilkan kata dari gerak dan hidup.

# ## Topic Modelling Menggunakan LSA

# Pada langkah sebelumnya adalah langkah langkah agar teks siap diproses pada langkah ini. Jadi pada langkah ini adalah langkah untuk melakukan pendekatan LSA. Pada dasarnya LSA adalah dekomposisi nilai tunggal

# In[22]:


from sklearn.decomposition import TruncatedSVD
lsa_model = TruncatedSVD(n_components=10, algorithm='randomized', n_iter=10, random_state=42)

lsa_top=lsa_model.fit_transform(vect_text)


# pada code diatas digunakan untuk memproses dekomposisi kalimat yang ada di Abstrak menggunakan TruncatedSVD lalu disimpan di dalam variabel bernama lsa_top

# In[23]:


print(lsa_top)
print(lsa_top.shape)  # (no_of_doc*no_of_topics)


# setelah itu dipanggil untuk ditampilkan seperti pada code diatas.

# In[24]:


l=lsa_top[0]
print("Document 0 :")
for i,topic in enumerate(l):
  print("Topic ",i," : ",topic*100)


# pada code diatas yang dipanggil hanya pada abstrak ke 1 atau pada code menggunakan index ke 0

# In[25]:


print(lsa_model.components_.shape) # (no_of_topics*no_of_words)
print(lsa_model.components_)


# setelah itu ditampilkan seperti pada code diatas

# In[26]:


# most important words for each topic
vocab = vect.get_feature_names()

for i, comp in enumerate(lsa_model.components_):
    vocab_comp = zip(vocab, comp)
    sorted_words = sorted(vocab_comp, key= lambda x:x[1], reverse=True)[:10]
    print("Topic "+str(i)+": ")
    for t in sorted_words:
        print(t[0],end=" ")
    print("\n")


# ketika code diatas itu dijalankan maka akan tampil topic topic seperti pada contoh diatas. lalu kita dapat menganalisis hasil dari code tersebut untuk langkah selanjutnya.
