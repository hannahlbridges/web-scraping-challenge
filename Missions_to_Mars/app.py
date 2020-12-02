from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_facts_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars_components = mongo.db.components.find_one()
    return render_template("index.html", mars_components=mars_components)


@app.route("/scrape")
def scraper():
    components = mongo.db.components
    mars_components = scrape_mars.scrape()
    components.update({}, mars_components, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)