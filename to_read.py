import pandas
import pandas as pd


def generate_recommendation(connection, user_id: int, number_recommendation: int):
    """
    Create a To_Read list of the favorite user's tag
    """
    pandas.set_option('display.max_rows',None)
    pandas.set_option('display.max_columns',None)

    # Get all tag id for the to read of our user
    df_tag = pd.read_sql(
        f"SELECT book_tags.tag_id FROM books INNER JOIN to_read on to_read.book_id = books.book_id INNER JOIN book_tags on book_tags.goodreads_book_id = books.goodreads_book_id WHERE to_read.user_id={user_id}",
        connection)
    # Get the most frequent tag
    recommended_tag = df_tag.tag_id.value_counts()[:1].index.tolist()

    # Look for all the books that have this tag
    df = pd.read_sql(f"SELECT books.title, books.average_rating, tags.tag_name, books.authors,books.original_publication_year, books.language_code,books.image_url  FROM books INNER JOIN book_tags ON books.goodreads_book_id = book_tags.goodreads_book_id INNER JOIN tags ON tags.tag_id = book_tags.tag_id WHERE tags.tag_id = {recommended_tag[0]}",
                      connection)
    # Sort by rating to get the best one
    df = df.sort_values(by=['average_rating'], ascending=False)
    df = df.head(number_recommendation)

    return df.to_dict(orient='records')
