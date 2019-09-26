from flask import Flask, abort, jsonify, render_template,url_for, request,send_from_directory,redirect
import numpy as np 
import pandas as pd 
import json
import requests 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity 

data = pd.read_json('DigiData.json')
def Comb(i):
    return str(i['stage'])+ '$' +str(i['type'])+'$'+str(i['attribute'])
data['x'] = data.apply(Comb, axis=1)
data['digimon']=data['digimon'].apply(lambda i: i.lower())

cov = CountVectorizer(tokenizer=lambda data: data.split('$'))
data1 = cov.fit_transform(data['x'])
DigiS = cosine_similarity(data1)

app = Flask(__name__)

#home
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/FoundDigi', methods=['GET', 'POST'])
def cari():
    body = request.form
    digi = body['digimon']
    digi = digi.lower()
    if digi not in list(data['digimon']):
        return redirect('/Not Found Dude')
    digind = data [data['digimon']==digi].index.values[0]
    favorit = data.iloc[digind][['digimon','stage','type','attribute','image']]
    Score = list(enumerate(DigiS[digind]))
    Digisort = sorted(Score, key=lambda i:i[1], reverse=True)
    reccomend = []
    for item in Digisort[:7]:
        x = {}
        if data.iloc[item[0]]['digimon'] !=digi:
            nama = data.iloc[item[0]]['digimon'].capitalize()
            stage = data.iloc[item[0]]['stage']
            gambar = data.iloc[item[0]]['image']
            Type = data.iloc[item[0]]['type']
            attribute = data.iloc[item[0]]['attribute']
            x['digimon'] = nama
            x['stage'] = stage
            x['image'] = gambar
            x['type'] = Type
            x['attribute'] = attribute
            reccomend.append(x)
    return render_template('home.html', reccomend=reccomend, favorit=favorit)

@app.route('/NotFound')
def error():
    return render_template('error.html')

if __name__=='__main__':
    app.run(debug=True)