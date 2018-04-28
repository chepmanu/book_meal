from flask import Flask, request, jsonify, abort, make_response

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ER9U9U9N9EUR'

from . import endpoints

