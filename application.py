from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
# from database_setup import Category, Base, CategoryItem, User
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

APPLICATION_NAME = "Catalog Application"

# engine = create_engine('sqlite:///catalog.db')
# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)
# session = DBSession()


@app.route('/')
def show_index():
    return "Hello World! This is Flask."


@app.route('/resume')
def parse_resume():
    resstr = ""
    if request.form['file']:
        resstr += "uploaded file"
    else:
        resstr += "no file"
    resstr += ("  " + str(request.form['optradio']))
    return resstr


app.secret_key = '89324heosrhg8943fji023u4r'

if __name__ == '__main__':

    app.debug = True
    app.run()
