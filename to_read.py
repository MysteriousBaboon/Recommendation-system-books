import pandas as pd
import collaborative as collab
import popularity


def generate_recommendation(connection, user_id: int, number_recommendation: int = 5):
    """
    Create a To_Read list of the favorite user's tag
    """

    # Get all tags id for the to read list of our user
    try:

        df_tag = pd.read_sql(
            f"SELECT book_tags.tag_id FROM books INNER JOIN to_read on to_read.book_id = books.book_id INNER JOIN "
            f"book_tags on book_tags.goodreads_book_id = books.goodreads_book_id WHERE to_read.user_id={user_id}",
            connection)

        # Get the most frequent tag
        recommended_tag = df_tag.tag_id.value_counts()[:1].index.tolist()

        # Look for all the books that have this tag
        df = pd.read_sql(
            f"SELECT books.title, books.best_book_id, books.average_rating, tags.tag_name, books.authors,"
            f"books.original_publication_year, books.language_code,books.image_url  FROM books INNER JOIN book_tags "
            f"ON books.goodreads_book_id = book_tags.goodreads_book_id INNER JOIN tags ON tags.tag_id = "
            f"book_tags.tag_id WHERE tags.tag_id = {recommended_tag[0]}",
            connection)
        # Get the chosen tag's name
        tag = df.tag_name.value_counts()[:1].index.tolist()[0]
        tag = str(tag)

    except:
        # If there is not enough data send instead a popularity list
        df = popularity.generate_recommendation(connection, number_recommendation)
        df = df.to_dict(orient='records')
        return df, None

    # Sort by rating to get the best one
    df = df.sort_values(by=['average_rating'], ascending=False)
    # Apply collaborative on pre selected books
    result = collab.clean_recommendation(df, user_id, number_recommendation)
    return result, tag
