import collaborative
import to_read
import mysql.connector as con
from jinja2 import Environment, FileSystemLoader

# User ID wanted for prediction
wanted_id = 4

# Get Database Credentials
f = open("credentials", "r")
credentials = f.readlines()

# Connection to the database
connection = con.connect(host='localhost', database='goodreads', user=credentials[2], password=credentials[3])
if connection.is_connected():
    db_Info = connection.get_server_info()
    print("Connected to MySQL Server version ", db_Info)


# Main Recommender function
def recommender(number_recommendation=5):
    # Collaborative Filtering
    collab = collaborative.generate_recommendation(connection, wanted_id, number_recommendation)

    plan_to_read, tag = to_read.generate_recommendation(connection, wanted_id, number_recommendation)
    print(plan_to_read)
    print(collab)
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    open("result.html", "w").write(env.get_template("template.html").render(collab=collab, to_read=plan_to_read, tag=tag))


recommender()
