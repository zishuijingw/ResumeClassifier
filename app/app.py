from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
import pandas as pd
import numpy as np
import time
import threading
import os
from data_clean import cleanHtml, cleanPunc, keepAlpha, removeStopWords, stemming, tf_idf
from model import perdicet_category

app = Flask(__name__)
Bootstrap(app)

# connect database
# app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/database_predictions"
# mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home', methods=['POST','GET'])
def home():
    if request.method=='POST':
        user_name = request.form['usr']
        # user_name = 'TEMP'
    else:
        user_name = ""
    return render_template('home.html', user_name=user_name)


@app.route('/multilabel', methods=['GET','POST'])
def multilabel():
    reminder = ''
    return render_template('multilabel_submit.html', reminder=reminder)

# results
@app.route('/multilabel_recommendations', methods=['GET','POST'])
def multilabel_recmomendations():
    errors=[]
    reminder = ''
    if request.method=='POST':
        # get url that the user has entered
        try:
            url = request.form['user_input_test']
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )

    data_raw = url

    if len(data_raw) <= 250:
        reminder = 'Please input more than 250 words'
        return render_template('multilabel_submit.html', reminder=reminder)

    test_data = pd.Series(np.array(data_raw.lower()))
    test_data = test_data.apply(cleanHtml)
    test_data = test_data.apply(cleanPunc)
    test_data = test_data.apply(keepAlpha)
    test_data = test_data.apply(removeStopWords)
    test_data = test_data.apply(stemming)

    print(test_data)
    # data = tf_idf(test_data)

    # predictions = perdicet_category(data)

    predictions = pd.read_csv('predictions_example.csv')

    prediction = predictions.loc[0].to_dict()

    return render_template('multilabel_recommendations.html', errors=errors, predictions=prediction)


# temp
@app.route('/results_lda', methods=['GET','POST'])
def lda():
    return render_template('results_lda.html')



# @app.route('/recommendations', methods=['GET','POST'])
# def recmomendations():
#     return render_template('recommendations.html')


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, debug=True)
        