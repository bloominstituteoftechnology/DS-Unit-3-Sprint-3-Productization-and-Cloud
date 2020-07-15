#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#pip install pickle-mixin


# In[1]:


#import the basics but important libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Sklearn Preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.tree import DecisionTreeClassifier

#import pickle
import pickle
import requests
import json


# In[2]:


#import





iris = pd.read_csv("https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/d546eaee765268bf2f487608c537c05e22e4b221/iris.csv")




# In[3]:


iris.head()


# In[4]:


iris.dtypes


# In[5]:


#check dist of y
plt.hist(iris['species'])
plt.show()


# In[6]:


#encode
le = LabelEncoder()
le.fit(iris['species'])


# In[7]:


iris['species'] = le.transform(iris['species'])


# In[8]:


#Features
x = iris.iloc[: , 0:4 ]
x.head()


# In[9]:


y = iris.iloc[:,4]
y.head()


# In[10]:


#split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = .25, random_state = 123)


# In[11]:


#model
algo = DecisionTreeClassifier()
model = algo.fit(x_train, y_train)


# In[12]:


#Predict
y_pred = model.predict(x_test)


# In[13]:


print(accuracy_score(y_test, y_pred))


# In[14]:


print(classification_report(y_test, y_pred))


# In[19]:


#pickle
pickle.dump(model, open('iris_model.pkl', 'wb'))


# In[20]:


my_model = pickle.load(open('iris_model.pkl', 'rb'))


# In[21]:


url = "https://localhost:9000/api"


# In[22]:


data = json.dumps({'sepal_width': 2.8, 'sepal_legnth': 6.3,'petal_width': 1.8,  'petal_legnth' : 5.5})


# In[24]:


send = requests.post(url, data)


# In[ ]:





# In[ ]:





# In[ ]:




