from flask import render_template, flash, redirect, url_for
from app import app, db

@app.route("/")
@app.route("/home")
def home():
  return render_template('home.html')

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/compare")
def compare():
  return render_template("compare.html")

@app.route("/top_ranks")
def topRanks():
  return render_template("top_ranks.html")

@app.route("/account")
def account():
  return render_template("account.html")

