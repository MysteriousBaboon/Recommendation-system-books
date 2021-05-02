import difflib
import random
import pickle

import pandas as pd

# Loading of the model
model = pickle.load(open('svdpickle.pt', 'rb'))


def get_book_id(book_title, metadata):
    """
    Gets the book ID for a book title based on the closest match in the metadata dataframe.
    """
    existing_titles = list(metadata['title'].values)
    closest_titles = difflib.get_close_matches(book_title, existing_titles)
    book_id = metadata[metadata['title'] == closest_titles[0]]['best_book_id'].values[0]
    return book_id


def get_book_info(book_id, metadata):
    """
    Returns some basic information about a book given the book id and the metadata dataframe.
    """
    book_info = metadata[metadata['best_book_id'] == book_id][[
        'authors', 'original_publication_year', 'title', 'language_code', 'average_rating', 'image_url']]
    return book_info.to_dict(orient='records')[0]


def predict_review(user_id, book_title, metadata):
    """
    Predicts the review (on a scale of 1-5) that a user would assign to a specific book.
    """
    book_id = get_book_id(book_title, metadata)
    review_prediction = model.predict(uid=user_id, iid=book_id)
    return review_prediction.est


def generate_recommendation(connection, user_id: int, number_recommendation: int, thresh=4):
    """
    Generate the recommendations based purely on Collaborative filtering
    """
    df = pd.read_sql(
        f"SELECT ratings.user_id, books.best_book_id, books.authors, books.original_publication_year, "
        f"books.language_code, books.title, books.average_rating, books.image_url FROM ratings INNER JOIN books on "
        f"ratings.book_id = books.book_id  WHERE ratings.user_id={user_id}",
        connection)

    book_titles = list(df['title'].values)
    random.shuffle(book_titles)
    recommended_books = []

    for book_title in book_titles:
        rating = predict_review(user_id, book_title, df)
        if rating >= thresh:
            if len(recommended_books) < number_recommendation:
                book_id = get_book_id(book_title, df)
                recommended_books.append(get_book_info(book_id, df))
            else:
                break

    return recommended_books


def clean_recommendation(df, user_id, thresh=4, number_recommendation=5):
    book_titles = list(df['title'].values)
    recommended_books = []

    for book_title in book_titles:
        rating = predict_review(user_id, book_title, df)
        if rating >= thresh:
            if len(recommended_books) < number_recommendation:
                book_id = get_book_id(book_title, df)
                recommended_books.append(get_book_info(book_id, df))
            else:
                break

    return recommended_books
