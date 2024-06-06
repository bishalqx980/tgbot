from flask import Flask, render_template
from threading import Thread

app = Flask(__name__)


@app.route('/')
def index():
  return render_template("index.html")


def run():
  app.run(host='0.0.0.0', port=80)

def alive():
  Thread(target=run).start()