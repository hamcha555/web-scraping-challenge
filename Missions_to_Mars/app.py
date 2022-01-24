from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    mars2 = mongo.db.mars9.find_one()
    return render_template("index.html", mars8=mars2)

@app.route("/scrape")
def scrape():
    mars3 = mongo.db.mars9
    mars4 = scrape_mars.scrape_info()
    mars3.update_one({},{"$set":mars4}, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
