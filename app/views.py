# views.py

from flask import render_template
from flask import Flask,request
from flaskext.mysql import MySQL
from collections import Counter
from app import app

from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *

@app.route('/')
def index():
    return render_template("index.html")
 
@app.route('/baseWords')
def baseIndex():
    return render_template("baseWords.html")
@app.route('/baseWords/listAll')
def listBaseWords():
    mysql = MySQL()
    mysql.init_app(app)
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("SELECT word from words")
    data = cursor.fetchall()
    data = [x[0] for x in data]
    data_count = Counter(data)
    return render_template("listWords.html", result = data_count)
@app.route('/baseWords', methods=['POST'])
def baseWordCount():
    lemmatizer = WordNetLemmatizer()
    word = lemmatizer.lemmatize(request.form['text'])
    print(word)
    stemmer = PorterStemmer()
    word = stemmer.stem(word)
    print(word)
    mysql = MySQL()
    mysql.init_app(app)
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "select word from words where word = %s"
    cursor.execute(sql,word)
    data = cursor.fetchall()
    data = [x[0] for x in data]
    data_count = Counter(data)
    return render_template("listWords.html", result = data_count)
    
    
@app.route('/nounVerb')
def nounVerbIndex():
    return render_template("nounVerb.html")
@app.route('/nounVerb/0')
def nounVerb0():
    mysql = MySQL()
    mysql.init_app(app)
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("SELECT word from words where book_ID = 0 and type = 'verb'")
    verb = cursor.fetchall()
    verb = [x[0] for x in verb]
    verb_count = Counter(verb)
    cursor.execute("SELECT word from words where book_ID = 0 and type = 'noun'")
    noun = cursor.fetchall()
    noun = [x[0] for x in noun]
    noun_count = Counter(noun)
    return render_template("listNounsVerbs.html", result1 = noun_count, result2 = verb_count)
@app.route('/nounVerb/1')
def nounVerb1():
    mysql = MySQL()
    mysql.init_app(app)
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("SELECT word from words where book_ID = 1 and type = 'verb'")
    verb = cursor.fetchall()
    verb = [x[0] for x in verb]
    verb_count = Counter(verb)
    cursor.execute("SELECT word from words where book_ID = 1 and type = 'noun'")
    noun = cursor.fetchall()
    noun = [x[0] for x in noun]
    noun_count = Counter(noun)
    return render_template("listNounsVerbs.html", result1 = noun_count, result2 = verb_count)  
@app.route('/nounVerb/2')
def nounVerb2():
    mysql = MySQL()
    mysql.init_app(app)
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("SELECT word from words where book_ID = 2 and type = 'verb'")
    verb = cursor.fetchall()
    verb = [x[0] for x in verb]
    verb_count = Counter(verb)
    cursor.execute("SELECT word from words where book_ID = 2 and type = 'noun'")
    noun = cursor.fetchall()
    noun = [x[0] for x in noun]
    noun_count = Counter(noun)
    return render_template("listNounsVerbs.html", result1 = noun_count, result2 = verb_count)
@app.route('/nounVerb/3')
def nounVerb3():
    mysql = MySQL()
    mysql.init_app(app)
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("SELECT word from words where book_ID = 3 and type = 'verb'")
    verb = cursor.fetchall()
    verb = [x[0] for x in verb]
    verb_count = Counter(verb)
    cursor.execute("SELECT word from words where book_ID = 3 and type = 'noun'")
    noun = cursor.fetchall()
    noun = [x[0] for x in noun]
    noun_count = Counter(noun)
    return render_template("listNounsVerbs.html", result1 = noun_count, result2 = verb_count)
@app.route('/nounVerb/All')
def nounVerbAll():
    mysql = MySQL()
    mysql.init_app(app)
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("SELECT word from words where type = 'verb'")
    verb = cursor.fetchall()
    verb = [x[0] for x in verb]
    verb_count = Counter(verb)
    cursor.execute("SELECT word from words where type = 'noun'")
    noun = cursor.fetchall()
    noun = [x[0] for x in noun]
    noun_count = Counter(noun)
    return render_template("listNounsVerbs.html", result1 = noun_count, result2 = verb_count) 
      
@app.route('/similarity')
def similarityIndex():
    return render_template("similarity.html")
@app.route('/similarity', methods=['POST'])
def similarityView():
    mysql = MySQL()
    mysql.init_app(app)
    conn = mysql.connect()
    cursor =conn.cursor()
    if request.form['book1'] != "4":
        sql = "SELECT similarity from similarities where book1_ID = %s and book2_ID = %s"
        cursor.execute(sql,(int(request.form['book1']),int(request.form['book2'])))
        return str(cursor.fetchall()[0][0])
    else:
        cursor.execute("SELECT * from similarities")
        data = cursor.fetchall()
        return render_template("listSimilarities.html", result = data) 

@app.route('/about')
def about():
    return render_template("about.html")

