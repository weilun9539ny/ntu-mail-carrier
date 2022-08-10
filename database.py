import psycopg2


# Define functions
def insert_user_data(user_data_list):
    """The format of 'user_data_list' is:
    [user_id, user_account, password, email_uid]"""
    # Connect the database
    connection = psycopg2.connect(
        database="d9v7utrhcs9uc2",
        user="jvfmxlbipqvxrd",
        password="c082530a6c4d1d130e7db89e15f8c135b1a358efbe22acd3bbb0f44624a6d4cc",
        host="ec2-34-200-35-222.compute-1.amazonaws.com",
        port="5432")
    cursor = connection.cursor()
    # Finish connecting the database

    # Insert the new data
    table_columns = ["user_id", "account", "password", "email_uid"]
    insert_query = f"INSERT INTO account {table_columns} VALUES (%s, %s, %s, %s);"
    cursor.execute(insert_query, user_data_list)
    connection.commit()
    cursor.close()
    return "ok"


def select_user_data(user_id):
    # Connect the database
    connection = psycopg2.connect(
        database="d9v7utrhcs9uc2",
        user="jvfmxlbipqvxrd",
        password="c082530a6c4d1d130e7db89e15f8c135b1a358efbe22acd3bbb0f44624a6d4cc",
        host="ec2-34-200-35-222.compute-1.amazonaws.com",
        port="5432")
    cursor = connection.cursor()
    # Finish connecting the database

    # Get user data
    select_query = "SELECT * FROM account WHERE user_id = %s"
    cursor.execute(select_query, (user_id, ))
    user_data = cursor.fetchone()
    # Finish getting user data
    return user_data


def update_last_uid(user_id, last_uid):
    # Connect the database
    connection = psycopg2.connect(
        database="d9v7utrhcs9uc2",
        user="jvfmxlbipqvxrd",
        password="c082530a6c4d1d130e7db89e15f8c135b1a358efbe22acd3bbb0f44624a6d4cc",
        host="ec2-34-200-35-222.compute-1.amazonaws.com",
        port="5432")
    cursor = connection.cursor()
    # Finish connecting the database

    # Update the data
    update_query = f"UPDATE account SET email_uid = {last_uid} WHERE user_id = {user_id}"
    cursor.execute(update_query)
    connection.commit()
    cursor.close()
    # Finish updating the data
# Finish defining functions


# Create the table
if __name__ == "__main__":
    connection = psycopg2.connect(
        database="d9v7utrhcs9uc2",
        user="jvfmxlbipqvxrd",
        password="c082530a6c4d1d130e7db89e15f8c135b1a358efbe22acd3bbb0f44624a6d4cc",
        host="ec2-34-200-35-222.compute-1.amazonaws.com",
        port="5432")
    cursor = connection.cursor()
    create_table_query = """CREATE TABLE account(
        user_index serial PRIMARY KEY,
        user_id VARCHAR (100) UNIQUE NOT NULL,
        account VARCHAR (50) UNIQUE NOT NULL,
        password VARCHAR (50) NOT NULL,
        email_uid NUMERIC NOT NULL
    );"""
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
# Finish creating the table
