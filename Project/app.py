from flask import Flask, render_template, url_for
app = Flask(__name__)

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

if __name__ == '__main__':
  app.run(debug=True)
