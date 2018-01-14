# -*- coding: utf-8 -*-
"""
    Flask-upload-dropzone
    ===================================
    Summary: flask file upload with Dropzone.js.
    Author: Grey Li
    Repository: https://github.com/helloflask/flask-upload-dropzone
    License: MIT
"""
import os

from flask import Flask, render_template, request

app = Flask(__name__)
app.config['UPLOADED_PATH'] = os.getcwd() + '/upload'


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        # print file
        for f in request.files.getlist('file'):
            return render_template('display.html')
            return "successfully upload file"
            # f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    return render_template('index3.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)