import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import glob
from uuid import uuid4
import subprocess
from text_process import extract_d,scam_check

#import language_check
#tool = language_check.LanguageTool('en-US')

UPLOAD_FOLDER = './test'
ALLOWED_EXTENSIONS = set(['docx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def serve():
    return render_template("index.html")


@app.route('/file', methods=['GET', 'POST'])
def upload_file():
    print("file")
    if request.method == 'POST':
        
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        #print(file)
        

        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return render_template('index.html')

    return render_template('index.html')

@app.route('/text', methods=['GET', 'POST'])
def upload_text():
    print("text")
    if request.method == 'POST' and 'textupload' in request.form:
        text = request.form['textupload']
        
        corrected=scam_check.modify(text)
        #matches = tool.check(text)
        #corrected = language_check.correct(text, matches)

        return render_template('index.html', correct=corrected)

    return render_template('index.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print("uf")
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)

