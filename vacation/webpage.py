from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Cruise

app = Flask(__name__)

engine = create_engine('sqlite:///curise.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def index():
    curises = session.query(Cruise).order_by(Cruise.date)
    return render_template('index.html', curises = curises)

@app.route('/cheap')
def cheap():
    curises = session.query(Cruise).order_by(Cruise.price)
    return render_template('index.html', curises = curises)    

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)