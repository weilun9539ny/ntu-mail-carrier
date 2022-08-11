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
    table_columns = '("user_id", "account", "password", "email_uid")'
    insert_command = f"INSERT INTO account {table_columns} VALUES (%s, %s, %s, %s);"
    cursor.execute(insert_command, user_data_list)
    connection.commit()
    cursor.close()
    return "ok"


def select_data(user_id="all"):
    """The output of this funtion is a list containing user data.
    E.g., [(1, user_id, "b092070XX", password, 2811), (2, user_id, ...)]"""
    # Connect the database
    connection = psycopg2.connect(
        database="d9v7utrhcs9uc2",
        user="jvfmxlbipqvxrd",
        password="c082530a6c4d1d130e7db89e15f8c135b1a358efbe22acd3bbb0f44624a6d4cc",
        host="ec2-34-200-35-222.compute-1.amazonaws.com",
        port="5432")
    cursor = connection.cursor()
    # Finish connecting the database

    # Get data
    if user_id != "all":
        select_command = "SELECT * FROM account WHERE user_id = %s"
        cursor.execute(select_command, (user_id, ))
    else:
        select_command = "SELECT * FROM account"
        cursor.execute(select_command)
    user_data = cursor.fetchall()
    cursor.close()
    # Finish getting user data
    return user_data


def update_user_info(user_id, last_uid=-999, account="unchanged", password="unchanged"):
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
    if last_uid != -999:
        update_command = 'UPDATE account SET email_uid = %s WHERE user_id = %s'
        cursor.execute(update_command, (last_uid, user_id, ))
    elif (account != "unchange") and (password != "unchange"):
        update_command = "UPDATE account SET password = %s WHERE user_id = %s AND account = %s"
        cursor.execute(update_command, (password, user_id, account, ))

    connection.commit()
    cursor.close()
    # Finish updating the data


def delete_data(user_id, account):
    connection = psycopg2.connect(
        database="d9v7utrhcs9uc2",
        user="jvfmxlbipqvxrd",
        password="c082530a6c4d1d130e7db89e15f8c135b1a358efbe22acd3bbb0f44624a6d4cc",
        host="ec2-34-200-35-222.compute-1.amazonaws.com",
        port="5432")
    cursor = connection.cursor()

    delete_command = "DELETE FROM account WHERE user_id = %s AND account = %s"
    cursor.execute(delete_command, (user_id, account))
    connection.commit()
    cursor.close()
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
    # create_table_command = """CREATE TABLE account(
    #     user_index serial PRIMARY KEY,
    #     user_id VARCHAR (100) UNIQUE NOT NULL,
    #     account VARCHAR (50) UNIQUE NOT NULL,
    #     password VARCHAR (50) NOT NULL,
    #     email_uid NUMERIC NOT NULL
    #     );"""
    # cursor.execute(create_table_command)
    # cursor.execute("DELETE FROM account WHERE user_index = 3")
    cursor.execute("SELECT * FROM account")
    data = cursor.fetchall()
    print(data)
    # connection.commit()
    cursor.close()
# Finish creating the table
