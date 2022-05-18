from datetime import date
from flask import render_template


def cctv():
    today = date.today()
    print(today)
    return render_template('index.html', date=today)