import collaborative
import to_read
import pickle
import pandas as pd
import mysql.connector as con
from jinja2 import Environment, FileSystemLoader

# User ID wanted for prediction
wanted_id = 1

# Connection to the database
connection = con.connect(host='localhost', database='goodreads', user='mark', password='19991999')
if connection.is_connected():
    db_Info = connection.get_server_info()
    print("Connected to MySQL Server version ", db_Info)

# Loading of the model
svd = pickle.load(open('svdpickle_file', 'rb'))


# Main Recommender function
def recommender(number_recommendation=5):
    collab = collaborative.generate_recommendation(connection, wanted_id, svd, number_recommendation)
    plan_to_read = to_read.generate_recommendation(connection, wanted_id, number_recommendation)
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    open("result.html", "w").write(env.get_template("template.html").render(collab=collab, to_read=plan_to_read))


recommender()
