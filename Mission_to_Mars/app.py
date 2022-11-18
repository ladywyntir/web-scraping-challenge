
import scrape_4_mars
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)

# Use flask_PyMongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_info_db"
mongo = PyMongo(app)

@app.route("/")
def index():
        
    # set up a piece of info to display at the Index
    mars_index = mongo.db.marsData.find_one()

    # send output to the index.html file 
    return render_template("index.html", mars=mars_index)
    

@app.route("/scrape")
def scrape():
    # this will be a reference to our database collection (table)
    marsTable = mongo.db.marsData

    # in case the table exists, drop it
    mongo.db.marsData.drop()

    # call our scrape_all script from scrape_4_mars.py file
    mars_data = scrape_4_mars.scrape_all()

    # load dictionary into Mongo
    marsTable.insert_one(mars_data)

    # mars.update({},mars_data, upsert=True)
    return redirect('/', code=302)
    #return mars_data

if __name__ == "__main__":
    app.run()