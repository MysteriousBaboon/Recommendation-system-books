import pandas as pd


def generate_recommendation(connection):
    df = pd.read_sql(
        f"SELECT books.average_rating, books.authors, books.original_publication_year, books.language_code, books.title, books.image_url FROM books",
        connection)
    df = df.sort_values(by=['average_rating'], ascending=False)
    df = df.iloc[:5]

    return df


