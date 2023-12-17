import Extract
import Transform
import sqlalchemy
import sqlite3

LOCATION = "sqlite:///user_recently_played_tracks.sqlite"

if __name__ == "__main__":
    load_df = Extract.get_recently_played_track()
    print(load_df)
    if Transform.data_quality(load_df):
        raise Exception("Data Validation failed")
    transformed_df = Transform.transform(load_df)

    #Loading into database
    engine = sqlalchemy.create_engine(LOCATION)
    connection = sqlite3.connect("user_recently_played_tracks.sqlite")
    cursor = connection.cursor()

    #SQL Query for user's most recently played tracks
    sql_1 = """
    CREATE TABLE IF NOT EXISTS user_recently_played_tracks (
        id SERIAL,
        song_name VARCHAR(200),
        artist VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        PRIMARY KEY (id)
    );
    """

    #Sql Query for user's most recently listened artists
    sql_2 = """
    CREATE TABLE IF NOT EXISTS most_recently_listened_artists (
        id VARCHAR(200),
        timestamp VARCHAR(200),
        artist VARCHAR(200),
        count INTEGER,
        PRIMARY KEY (id)
    );
    """
    cursor.execute(sql_1)
    cursor.execute(sql_2)

    try:
        load_df.to_sql("user_recently_played_tracks", engine, index = False, if_exists = "append")
    except:
        print("Data already exists in database (user recently played tracks).")
    try:
        transformed_df.to_sql("most_recently_listened_artists", engine, index = False, if_exists = "append")
    except:
        print("Data already exists in database (most recently listened artists).")

    connection.close()