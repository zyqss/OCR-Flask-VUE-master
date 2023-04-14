from flask import render_template, jsonify, request
import requests
from random import *
import init
# from backup.database import Article, session
import json

app = init.create_app()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")


@app.route('/api/login', methods=['GET', 'POST'])
def login():
    username = request.values.get('username')
    password = request.values.get('password')
    if username == 'user1' and password == 'pass1':
        res = {
            'isLogin': '0',
            'msg': 'success'
        }
        return jsonify(res)
    else:
        res = {
            'isLogin': '-1',
            'msg': 'fail'
        }
        return jsonify(res)



if __name__ == '__main__':
    app.run(debug=True)
