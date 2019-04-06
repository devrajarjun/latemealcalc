from flask import Flask, render_template
import os
import psycopg2
import subprocess

import os

app = Flask(__name__, static_url_path = "", static_folder = "static")

#'heroku config:get DATABASE_URL -a calculatemeal' to get the name of the database
DATABASE_URL = 'postgres://gniojkvxziujuu:1c53b1d388891669097c66f2e618d42e31ffffa249aaaef45ccf72034503106c@ec2-184-73-153-64.compute-1.amazonaws.com:5432/d1ipk1vqr3fslq'

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()
cursor.execute(
  """
  CREATE TABLE food (
    name VARCHAR(50) NOT NULL PRIMARY KEY,
    price REAL NOT NULL,
    category VARCHAR(50) NOT NULL,
    count INTEGER NOT NULL
  )
  """)
cursor.execute(
    """
    INSERT INTO food (name, price, category, count)
        VALUES ('peanuts', 2.50, 'packaged', 0), ('sausage pizza', 5.00, 'pizza', 0), ('cheese pizza', 5.00, 'pizza', 0), ('waffles', 4.00, 'grill', 0), ('grapes', 4.00, 'packaged', 0), ('fries', 2.30, 'grill', 0)
    """)

@app.route("/")
def main():
    return render_template("index.html")
  
@app.route("/contact")
def getContact():
    return render_template("contact.html")
  
@app.route("/favorites")
def getFavorites():
    return render_template("favorites.html")

@app.route("/info")
def getInfo():
    return render_template("info.html")
  
@app.route("/search/item/<item>")
def getItem(item):
  cursor.execute("SELECT name FROM food")
  results = cursor.fetchall()
  retVal = ""
  if len(results) == 0:
    return "No results found."
  for re in results:
      if item in str(re):
          retVal = retVal + str(re)
    
  return render_template("results.html", resultStr = retVal)


@app.route("/search/category/<catg>")
def getItemsFromCategory(catg):
  '''
  cursor.execute("SELECT name, category FROM food WHERE category = $1", [catg])
  results = cursor.fetchall()
  if len(results) == 0:
    return "No results found."
  retVal = "Category: " + catg + "\n"
  for re in results:
      retVal = retVal + str(re[0])
  return retVal'''
  return render_template("category1.html")

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(debug=False, port=PORT, host='0.0.0.0')
