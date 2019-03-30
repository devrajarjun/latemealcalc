from flask import Flask, render_template
import os
import psycopg2
import subprocess

import os

app = Flask(__name__)

#'heroku config:get DATABASE_URL -a calculatemeal' to get the name of the database
DATABASE_URL = 'postgres://gniojkvxziujuu:1c53b1d388891669097c66f2e618d42e31ffffa249aaaef45ccf72034503106c@ec2-184-73-153-64.compute-1.amazonaws.com:5432/d1ipk1vqr3fslq'

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()
cursor.execute(
  """
  CREATE TABLE food (
    foodname VARCHAR(50) NOT NULL PRIMARY KEY,
    price REAL NOT NULL,
    type VARCHAR(50) NOT NULL,
    count INTEGER NOT NULL
  )
  """)
cursor.execute(
    """
    INSERT INTO food (foodname, price, type, count)
        VALUES ('peanuts', 2.50, 'packaged', 0), ('pizza', 5.00, 'pizza', 0), ('waffles', 4.00, 'grill', 0), ('grapes', 4.00, 'packaged', 0), ('fries', 2.30, 'grill', 0)
    """)

@app.route("/")
def main():
    html = "<html><body>"
    cursor.execute('''SELECT * FROM food''')
    query = cursor.fetchone()
    # while query:
    html += "<p>" + query[0] + " " + query[1] + " " + query[2] + " " + query[3] + "</p>"
        # query = cursor.fetchone()
    
    html += "</body></html>"
    return html

@app.route("/<item>")
def search(item):
    cursor.execute("SELECT * FROM food WHERE foodname='%s'" % item)
    query = cursor.fetchone()
    if query == None:
        html = "No such item was found"
    else:
        html = query[0] + " " + query[1] + " " + query[3]
        # cursor.execute("UPDATE food SET count=count+1 WHERE foodname='%s'" % item)
        # cursor.commit()
    
    return html

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(debug=False, port=PORT, host='0.0.0.0')