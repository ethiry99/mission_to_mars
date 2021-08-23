# Let's break down what this code is doing.

# The first line says that we'll use Flask to render a template, redirecting to another url, and creating a URL.
# The second line says we'll use PyMongo to interact with our Mongo database.
# The third line says that to use the scraping code, we will convert from Jupyter notebook to Python.


from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# Under these lines, let's add the following to set up Flask:

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection

# app.config["MONGO_URI"] tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL.

# "mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo. This URI is saying that the app can reach 
            # Mongo through our localhost server, using port 27017, using a database named "mars_app".

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#declare home page, root page.

@app.route("/")


def index():

   #mars = mongo.db.mars.find_one() uses PyMongo to find the "mars" collection in our database,
        #  which we will create when we convert our Jupyter scraping code to Python Script. 
        # We will also assign that path to themars variable for use later. 
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

 # define /scrape page  
 @app.route("/scrape")

def scrape():

#Then, we assign a new variable that points to our Mongo database: mars = mongo.db.mars.#
   mars = mongo.db.mars

 #Next, we created a new variable to hold the newly scraped data: mars_data = scraping.scrape_all(). 
 # In this line, we're referencing the scrape_all function in the scraping.py file exported from Jupyter Notebook.  
   mars_data = scraping.scrape_all()

 #Now that we've gathered new data, we need to update the database using .update(). 
 # Let's take a look at the syntax we'll use, as shown below:
 # We're inserting data, so first we'll need to add an empty JSON object with {} in place of the query_parameter.
 #  Next, we'll use the data we have stored in mars_data. Finally, the option we'll include is upsert=True. 
 # This indicates to Mongo to create a new document if one doesn't already exist, and new data will always be saved
 #  (even if we haven't already created a document for it).
 
   mars.update({}, mars_data, upsert=True)
#Finally, we will add a redirect after successfully scraping the data: return redirect('/', code=302). 
 #This will navigate our page back to / where we can see the updated content.
 #   

   return redirect('/', code=302)  

 #The final bit of code we need for Flask is to tell it to run. 

if __name__ == "__main__":
   app.run()  