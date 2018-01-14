from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, send_from_directory
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, JOBS
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import textract

import os
from werkzeug import secure_filename

import gensim

ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)

APPLICATION_NAME = "Catalog Application"

app.config['UPLOAD_FOLDER'] = "/var/www/pdfs/"
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

model = gensim.models.Word2Vec.load('/var/www/myresume2jobs/w2v.model')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

engine = create_engine('mysql+pymysql://job:123@localhost:3306/JOB')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# app.config['UPLOADED_PATH'] = os.getcwd() + '/upload'


@app.route('/')
def show_index():
    return render_template('index.html')


# @app.route('/display/<filename>')
# def display_content(filename):
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     text = textract.process(str(file_path), encoding='ascii')
#     return render_template('display.html', text=str(text))


@app.route('/resume', methods=['POST', 'GET'])
def parse_resume():

    # resstr = ""
    if request.method == 'POST':
        if request.files['file']:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                return "resume saved"

        else:
            text = "no file"
            return render_template('display.html', text=text)
    else:
        filename = request.args.get('filename')
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        text = textract.process(str(file_path), encoding='ascii')
        text = text.replace("\n", " ")
        text = text.replace(".", " ")
        text = text.replace(",", " ")
        resume_parse = text.split()
        if request.form['optradio'] == "jobs":
            jobs = session.query(JOBS).filter_by(Job=1).all()
            jobs_distance = []
            for job in jobs:
                job_description = job.Description
                job_description = text.replace("\n", " ")
                job_description = text.replace(".", " ")
                job_description = text.replace(",", " ")
                job_description_parse = job_description.split()
                distance = model.wmdistance(
                    resume_parse, job_description_parse)
                jobs_distance.append((distance, job.JobLink))

            results = sorted(jobs_distance, key=lambda x: x[0])[:20]
            jobs_results = []
            for result in results:
                jobs_results.append(session.query(
                    JOBS).filter_by(JobLink=result[1]).one())
            return render_template('display.html', jobs=jobs_results)

        else:
            jobs = session.query(JOBS).filter_by(Job=0).all()
            jobs_distance = []
            for job in jobs:
                job_description = job.Description
                job_description = text.replace("\n", " ")
                job_description = text.replace(".", " ")
                job_description = text.replace(",", " ")
                job_description_parse = job_description.split()
                distance = model.wmdistance(
                    resume_parse, job_description_parse)
                jobs_distance.append((distance, job.JobLink))
            if len(jobs) < 20:
                results = sorted(jobs_distance, key=lambda x: x[0])
            else:
                results = sorted(jobs_distance, key=lambda x: x[0])[:20]

            jobs_results = []
            for result in results:
                jobs_results.append(session.query(
                    JOBS).filter_by(JobLink=result[1]).one())
            return render_template('display.html', jobs=jobs_results)


app.secret_key = '89324heosrhg8943fji023u4r'

if __name__ == '__main__':

    app.debug = True
    app.run()
