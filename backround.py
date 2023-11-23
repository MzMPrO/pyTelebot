from threading import Thread

from flask import Flask

from main import start_bot

app = Flask('')


@app.route('/')
def home():
    return "I'm alive"


def run():
    app.run(host='0.0.0.0', port=80)


def keep_alive():
    t2 = Thread(target=start_bot)
    t2.start()


keep_alive()
