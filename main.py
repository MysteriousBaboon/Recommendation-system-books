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
    # Plan to read using tag and Collaborative Filtering
    plan_to_read, tag = to_read.generate_recommendation(connection, wanted_id, number_recommendation)

    # Open the folder templates
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    # Write a Html page based on template.html and passing it the List of books that passed through
    # - Collaborative filtering
    # - To Read Collaborative filtering (if there is no tag, pass Popularity instead)
    # - And the best tag
    open("result.html", "w").write(env.get_template("template.html").render(collab=collab, to_read=plan_to_read, tag=tag))


recommender()
