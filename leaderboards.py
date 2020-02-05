import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)

        sql_create_index = "CREATE INDEX IF NOT EXISTS score_index ON leaderboard" \
                           "( score DESC " \
                           ");"
        c.execute(sql_create_index)

    except Error as e:
        print(e)

def insert_score(conn, score, name):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    #sql = """ INSERT INTO leaderboard(name,score)
    #          VALUES($name,score) """

    #Create a cursor
    cur = conn.cursor()

    #Add the record
    cur.execute(" INSERT INTO leaderboard(person_name,score) VALUES(?,?)", (name,int(score)))

    #Commit the changes to the DB
    conn.commit()

    cur.execute("DROP INDEX score_index;")

    sql_create_index = "CREATE INDEX IF NOT EXISTS score_index ON leaderboard" \
                       "( score DESC " \
                       ");"

    cur.execute(sql_create_index)

    #Close the cursor
    cur.close()

def checkExists():
    database = r"BitRacer_Leaderboard.db"

    conn = create_connection(database)

    cur = conn.cursor()

    check_if_table_exists = '''SELECT count(*) FROM sqlite_master WHERE type='table' AND name='leaderboard';'''

    cur.execute(check_if_table_exists)



    if cur.fetchone()[0] == 1:
        # commit the changes to db
        conn.commit()
        # close the connection
        conn.close()
        return True
    else:
        # commit the changes to db
        conn.commit()
        # close the connection
        conn.close()
        return False




def getAll():

    database = r"BitRacer_Leaderboard.db"

    conn = create_connection(database)


    sql_get_top_five = "SELECT * FROM leaderboard ORDER BY score DESC LIMIT 5;"

    cur = conn.cursor()


    cur.execute(sql_get_top_five)

    rows = cur.fetchall()

    conn.commit()
    conn.close()

    return rows
    
def insert(score, name):
    database = r"BitRacer_Leaderboard.db"

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS leaderboard (
                                        person_name text NOT NULL,
                                        score INT NOT NULL
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)
        insert_score(conn, score, name)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    exit()