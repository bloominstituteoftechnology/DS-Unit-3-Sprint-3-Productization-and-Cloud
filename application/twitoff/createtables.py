def Create():

    import sqlite3
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    query = '''
        CREATE TABLE IF NOT EXIST
            user (
                id integer PRIMARY KEY,
                name text NOT NULL,
                newest_tweet_id integer
            );
            
        CREATE TABLE IF NOT EXIST
            user (
                id integer PRIMARY KEY,
                name text NOT NULL,
                embedding integer
            );  
        '''

    c.execute(query)

    conn.commit()
    conn.close()
