#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
data = pd.read_csv('data_awal_crawling.csv')


# In[2]:


data.dropna(inplace=True)
data.isnull().sum()


# In[3]:


data.to_excel("hasil_crawling.xlsx")


# In[ ]:




