from flask import Flask, render_template, request, redirect, session, flash, url_for
import json

import requests

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/twt')
def twt():

    return "hello world"

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=8080, debug=True)