# coding:utf-8

import os
import time
from datetime import timedelta

from django.shortcuts import render
import cv2
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import detect

# set allowed file types
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp','jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)
# set time
app.send_file_max_age_default = timedelta(seconds=1)


def count():
    n = [0] * 22
    # 14=bird 15=cat 16=dog 17=horse 18=sheep 19=cow 20=elephant 21=bear
    animals = [''] * 14 + ['bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear']
    s = 'In this image, there are:\n'
    index = 0
    text_dir = './static/images/detected/result.txt'
    with open(text_dir) as text_file:
        for line in text_file:
            list1 = line.rstrip('\n').split(' ')
            label = list1[0]
            n[int(label)] += 1
        text_file.close()
        print(n)
    for i in n:
        if i != 0:
            print(index, '--', str(i))
            substring = str(i) + " " + animals[index] + "(s)"
            s = s + '\n' + substring
        index += 1
    if s == 'In this image, there are:\n':  # if nothing in the picture
        s = 'No animal is detected!'
    return s


# @app.route('/upload', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])  # add route
def upload():
    if request.method == 'POST':
        f = request.files['file']

        #if not (f and allowed_file(f.filename)):
        #    return jsonify({"error": 1001, "msg": "Only file of png、PNG、jpg、JPG、bmp can be uploaded."})

        user_input = request.form.get("name")

        basepath = os.path.dirname(__file__)  # current path

        upload_path = os.path.join(basepath, 'static/images/origin/org.jpg')  # attention：create file dir first
        for file in os.listdir(os.path.join(basepath, 'static/images/origin')):
            os.remove(os.path.join(basepath, 'static/images/origin', file))
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')

        f.save(upload_path)

        detect.main(opt='')

        return render_template('detect.html', text=count())

    return render_template('index.html')


@app.route('/log',methods=["POST","GET"])
def log():
    value = request.get_json()
    print(value)
    if str(value) != "None":
        feedback_path = os.path.join(os.path.dirname(__file__), "static/feedback.txt")
        text = open(feedback_path, 'a')
        text.write(
            str(time.strftime('%d.%m.%Y %H:%M:%S', time.localtime(time.time()))) + str(
                value) + "\n")
        print(value)
        text.close()
    print('done')
    return render_template('index.html')


if __name__ == '__main__':
    # app.debug = True
    print(count())
    app.run(host="0.0.0.0", port=5000)
