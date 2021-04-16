import collaborative
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
    df = pd.read_sql(
        f"SELECT ratings.user_id, books.best_book_id, books.authors, books.original_publication_year, books.language_code, books.title, books.average_rating, books.image_url FROM ratings Inner Join books on ratings.book_id = books.book_id  WHERE ratings.user_id={wanted_id}",
        connection)

# Loading of the model
svd = pickle.load(open('svdpickle_file', 'rb'))


# Main Recommender function
def recommender(data, number_recommendation=5):
    collab = collaborative.generate_recommendation(wanted_id, svd, data, number_recommendation)
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    open("result.html", "w").write(env.get_template("template.html").render(collab=collab))


recommender(df)
