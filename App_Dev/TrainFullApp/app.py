# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 14:44:24 2018

@author: rendorHaevyn
@about: Flask Train Full App
@url: https://developer.okta.com/blog/2018/07/12/flask-tutorial-simple-user-registration-and-login
"""

## ----- IMPORTS ----- ##

from flask import Flask, render_template, g, redirect, url_for
from pathlib import Path
import os
import sys
import pandas as pd

CWD             = 'e:\\Documents\\GitHub\\AdjustedR2\\App_Dev\\TrainFullApp'
sys.path.append(CWD)
sys.path

from app_processing import *

# ROOT        = Path(__file__).parents[3]
try:
    ROOT        = Path('e:\Documents\GitHub')
except NameError:
    ROOT        = 'e:\\Documents\\GitHub'

F_SECRET        = 'flask_secret_key.txt'

## ----- LOAD KEYS ----- ##
#''.join(random.choices(string.ascii_uppercase + string.digits, k=100))

# Flask secret random key
with open(os.path.join(ROOT,F_SECRET),'r') as f_in:
    secret_key = f_in.readline()


## ----- LOAD TRAIN STATIONS ----- ##
ds = pd.read_csv(os.path.join(CWD,'data','train_stations.csv'))

station_dict = dict()
for word in sorted(ds.stop_name):
#    word = word[:10]
    f = word[0]
    if f in station_dict.keys():
        station_dict[f].append(word)
    else:
        station_dict[f] = [word]


## ----- CONSTANTS ----- ##
FLASK_SECRET_KEY    = secret_key


## ----- LOAD DATA ----- ##
df_bus, df_train, df_tram = load_data_chk()

## ----- APP CONFIGURATION ----- ##

app = Flask(__name__)
app.config["SECRET_KEY"] = FLASK_SECRET_KEY

## ----- APP DEFINITIONS ----- ##

#@app.before_request
#def before_request():
#    if oidc.user_loggedin:
#        g.user = okta_client.get_user(oidc.user_getfield("sub"))
#    else:
#        g.user = None


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", station_dict=station_dict)


@app.route("/dashboard")
#@oidc.require_login
def dashboard(): 
    script, div = bokeh_magic(df_bus, df_train, df_tram)
    
    return render_template("dashboard.html", script=script, div=div, station_dict=station_dict)


@app.route("/login")
#@oidc.require_login
def login():
    return redirect(url_for(".dashboard"))


@app.route("/logout")
def logout():
#    oidc.logout()
    return redirect(url_for(".index"))


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)

## HOW TO ##
# 1. CD to root directory of app.py
# 2. run " python app.py flask run"
# or: just hit F5 here!