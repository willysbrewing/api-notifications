# [START app]
import logging

from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():
    return 'Notifications Service'
