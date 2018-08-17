
# coding: utf-8

# In[1]:


from nltk.tokenize import word_tokenize

#Reading in words from
#The Notebooks of Leonardo Da Vinci
leonardo_words = word_tokenize(open('5000-8.txt', 'r', encoding = "ISO-8859-1").read())

#The Outline of Science, Vol. 1 (of 4) by J. Arthur Thomson
arthur_words   = word_tokenize(open('20417.txt', 'r').read())

#Ulysses by James Joyce
james_words    = word_tokenize(open('4300-0.txt', 'r').read())

#The Picture of Dorian Gray by Oscar Wilde
oscar_words    = word_tokenize(open('174.txt', 'r').read())


# In[2]:


#removing single characters and everything else but alphabets from strings and
#turning strings to lower cases
import re
alphatize = lambda x: re.sub('[^a-zA-Z]+', '', x)
words1 = [alphatize(x).lower() for x in leonardo_words if alphatize(x) != "" and len(alphatize(x)) != 1]
words2 = [alphatize(x).lower() for x in arthur_words   if alphatize(x) != "" and len(alphatize(x)) != 1]
words3 = [alphatize(x).lower() for x in james_words    if alphatize(x) != "" and len(alphatize(x)) != 1]
words4 = [alphatize(x).lower() for x in oscar_words    if alphatize(x) != "" and len(alphatize(x)) != 1]


# In[3]:


#Choose to use predefined list from python nltk plus added some garbage words from the book
stop_words = ["me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "done", "should", "now"]


# In[4]:


#removing stop words from the list of words
no_stop_words1 = [word for word in words1 if word not in stop_words]
no_stop_words2 = [word for word in words2 if word not in stop_words]
no_stop_words3 = [word for word in words3 if word not in stop_words]
no_stop_words4 = [word for word in words4 if word not in stop_words]


# In[5]:


#Choose to lemmetize as lemmetizing does not only cut off the end part but reduces to base form
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

lemmatized_words1 = [lemmatizer.lemmatize(x) for x in no_stop_words1]
lemmatized_words2 = [lemmatizer.lemmatize(x) for x in no_stop_words2]
lemmatized_words3 = [lemmatizer.lemmatize(x) for x in no_stop_words3]
lemmatized_words4 = [lemmatizer.lemmatize(x) for x in no_stop_words4]


# In[6]:


from nltk.stem.porter import *
stemmer = PorterStemmer()

stemmed_words1 = [stemmer.stem(x) for x in lemmatized_words1]
stemmed_words2 = [stemmer.stem(x) for x in lemmatized_words2]
stemmed_words3 = [stemmer.stem(x) for x in lemmatized_words3]
stemmed_words4 = [stemmer.stem(x) for x in lemmatized_words4]


# In[7]:


from nltk.corpus import wordnet as wn

def speech(x):
    if(wn.synsets(x) == []):
        return "none"
    elif(wn.synsets(x)[0].pos() == "n"):
        return "noun"
    elif(wn.synsets(x)[0].pos() == "v"):
        return "verb"
    else:
        return "none"



# In[8]:


import mysql.connector
cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='connectavo')
cursor = cnx.cursor()
cursor.execute("CREATE TABLE books (book_ID int NOT NULL PRIMARY KEY,name VARCHAR(255))")
sql = "INSERT INTO books (book_ID, name) VALUES (%s, %s)"
val = [(0,"The Notebooks of Leonardo Da Vinci"),
      (1,"The Outline of Science, Vol. 1 (of 4) by J. Arthur Thomson"),
      (2,"Ulysses by James Joyce"),
      (3,"The Picture of Dorian Gray by Oscar Wilde")]
cursor.executemany(sql,val)
cnx.commit()


# In[9]:


cursor.execute("CREATE TABLE words (word_ID int NOT NULL PRIMARY KEY, word VARCHAR(255), type VARCHAR(255), book_ID int ,FOREIGN KEY (book_ID) REFERENCES books(book_ID))")
sql = "INSERT INTO words (word_ID, word, type, book_ID) VALUES (%s, %s, %s, %s)"

word_ID = list(range(len(lemmatized_words1)+len(lemmatized_words2)+
                len(lemmatized_words3)+len(lemmatized_words4)))
words = lemmatized_words1+lemmatized_words2+lemmatized_words3+lemmatized_words4
types = [speech(x) for x in words]
words = stemmed_words1+stemmed_words2+stemmed_words3+stemmed_words4
book_ID = [0] * len(lemmatized_words1) + [1] * len(lemmatized_words2) + [2] * len(lemmatized_words3) + [3] * len(lemmatized_words4)
vals = zip(word_ID,words,types,book_ID)
for val in vals:
    cursor.execute(sql,val)
    cnx.commit()


# In[10]:


import gensim
from gensim.models import TfidfModel

dictionary = gensim.corpora.Dictionary([lemmatized_words1,lemmatized_words2,lemmatized_words3,lemmatized_words4])
corpus = [dictionary.doc2bow(lemmatized_words1),dictionary.doc2bow(lemmatized_words2),
          dictionary.doc2bow(lemmatized_words3),dictionary.doc2bow(lemmatized_words4)]

tf_idf = TfidfModel(corpus)


sims = gensim.similarities.MatrixSimilarity(tf_idf[corpus])

query_doc_bow1 = dictionary.doc2bow(lemmatized_words1)
query_doc_bow2 = dictionary.doc2bow(lemmatized_words2)
query_doc_bow3 = dictionary.doc2bow(lemmatized_words3)
query_doc_bow4 = dictionary.doc2bow(lemmatized_words4)
query_doc_tf_idf1 = tf_idf[query_doc_bow1]
query_doc_tf_idf2 = tf_idf[query_doc_bow2]
query_doc_tf_idf3 = tf_idf[query_doc_bow3]
query_doc_tf_idf4 = tf_idf[query_doc_bow4]
similarity1 = sims[query_doc_tf_idf1]
similarity2 = sims[query_doc_tf_idf2]
similarity3 = sims[query_doc_tf_idf3]
similarity4 = sims[query_doc_tf_idf4]


# In[11]:


cursor.execute("CREATE TABLE similarities (book1_ID int, book2_ID int, similarity float(7,4), FOREIGN KEY (book1_ID) REFERENCES books(book_ID), FOREIGN KEY (book2_ID) REFERENCES books(book_ID))")


sql = "INSERT INTO similarities (book1_ID, book2_ID, similarity) VALUES (%s, %s, %s)"
vals = [(0,0,similarity1[0]*100),(0,1,similarity1[1]*100),(0,2,similarity1[2]*100),(0,3,similarity1[3]*100),
        (1,0,similarity2[0]*100),(1,1,similarity2[1]*100),(1,2,similarity2[2]*100),(1,3,similarity2[3]*100),
        (2,0,similarity3[0]*100),(2,1,similarity3[1]*100),(2,2,similarity3[2]*100),(2,3,similarity3[3]*100),
        (3,0,similarity4[0]*100),(3,1,similarity4[1]*100),(3,2,similarity4[2]*100),(3,3,similarity4[3]*100)
       ]

cursor.executemany(sql,vals)
cnx.commit()

