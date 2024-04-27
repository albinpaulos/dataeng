import pymysql

def search_users(username):
    # Vulnerable SQL query construction
    query = "SELECT * FROM users WHERE username='" + username + "'"
    
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='password',
                                 database='my_database',
                                 cursorclass=pymysql.cursors.DictCursor)
    
    try:
        with connection.cursor() as cursor:
            # Execute the SQL query
            cursor.execute(query)
            # Fetch the results
            result = cursor.fetchall()
            return result
    finally:
        # Close the database connection
        connection.close()

if __name__ == '__main__':
    # Prompt the user to enter a username
    user_input = input("Enter a username to search: ")
    # Search for the specified user
    users = search_users(user_input)
    # Display the search results
    for user in users:
        print(user)
