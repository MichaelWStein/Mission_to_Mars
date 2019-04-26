#Setting up flask

from flask import Flask, render_template, redirect
import pymongo
import scrape_mars as scrape

#Setting up the connection to the Mongo database
conn = 'mongodb://localhost:27017/'
client = pymongo.MongoClient(conn)
db = client.mars_db
col = db.info

app = Flask(__name__)

@app.route("/")
def home():
        mars_data = col.find_one()
        return render_template("index.html", data = mars_data)

@app.route("/scrape")
def data_storage(): 

        col.drop()

        #Scraping the Web and storing the information in results. 
        results = scrape.scrape()
        col.insert_one(results)
    
    #return
        return redirect("/")

if __name__ == "__main__":
        app.run(debug=True)