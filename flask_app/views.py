from flask import request, redirect, url_for, render_template, flash, session
from flask_app import app


@app.route('/')
def show_entries():
    return render_template('entries/index.html')

@app.route('/outcome', methods = ['GET', 'POST'])
def outcome():
    return render_template('outcome.html')

