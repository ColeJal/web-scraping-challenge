from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

#mongo = PyMongo(app, url="mongodb://localhost:27017/mars_app")
app.config["MONGO_URI"] ="mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_mission = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars_mission)


@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape_info()
    mongo.db.mars.update_one({}, {"$set": mars_data}, upsert=True)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)