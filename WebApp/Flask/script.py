import os
import numpy as np
import pandas as pd
import flask
import pickle
from sklearn.preprocessing import MinMaxScaler
from sklearn.externals import joblib 
from flask import Flask, render_template, request

#creating instance of the class
app=Flask(__name__)

#to tell flask what url shoud trigger the function index()
@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')

def ValuePredictorBinary(to_predict_list):
    print(to_predict_list)
    scaler = joblib.load("scaler_model.pkl")
    to_predict_df = pd.DataFrame([to_predict_list])
    to_predict_scaled = scaler.transform(to_predict_df)
    print(to_predict_scaled)
    to_predict = pd.DataFrame(to_predict_scaled)
    knnmodel = pickle.load(open("knnmodel.pkl","rb"))
    result = knnmodel.predict(to_predict)
    return result[0]

def ValuePredictorMulti(to_predict_list):
    print(to_predict_list)
    scaler = joblib.load("scaler_model_multi.pkl")
    to_predict_df = pd.DataFrame([to_predict_list])
    to_predict_scaled = scaler.transform(to_predict_df)
    print(to_predict_scaled)
    to_predict = pd.DataFrame(to_predict_scaled)
    knnmodel = pickle.load(open("knnmodelmulti.pkl","rb"))
    result = knnmodel.predict(to_predict)
    return result[0]
    
@app.route('/result_binary',methods = ['POST'])
def result_binary():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list=list(to_predict_list.values())
        result = ValuePredictorMulti(to_predict_list)
        if int(result)==1:
            prediction='Its an attack!'
        else:
            prediction='Its not an attack :)'
        return render_template("result.html",prediction=prediction)
    
@app.route('/result_multi',methods = ['POST'])
def result_multi():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list=list(to_predict_list.values())
        result = ValuePredictorBinary(to_predict_list)
        result = int(result)
        print(result)
        if result==0:
            prediction='Normal attack'
        elif result==1:
            prediction='Reconnaissance attack'
        elif result==2:
            prediction='Backdoor attack'
        elif result==3:
            prediction='DoS attack'
        elif result==4:
            prediction='Exploits attack'
        elif result==5:
            prediction='Analysis attack'
        elif result==6:
            prediction='Fuzzers attack'
        elif result==7:
            prediction='Worms attack'
        elif result==8:
            prediction='Shellcode attack'
        else:
            prediction='Generic attack'
        return render_template("result.html",prediction=prediction)
