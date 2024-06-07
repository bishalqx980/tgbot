import os
from threading import Thread
from flask import Flask, render_template

app = Flask(__name__)
PORT = int(os.environ.get("PORT", 8080))

@app.route('/')
def index():
  return render_template("index.html")

def run():
  app.run(host='0.0.0.0', port=PORT)

def alive():
  Thread(target=run).start()