import argparse
import sqlite3
import pymysql

def get_user_inputs(args):
    # Collect SQLite database details
    sqlite_db_path = args.sqlite if args.sqlite else input("Enter the path to the SQLite database file: ")
    
    # Collect MySQL database details
    mysql_server = args.server if args.server else input("Enter the MySQL server address: ")
    mysql_username = args.username if args.username else input("Enter the MySQL username: ")
    mysql_password = args.password if args.password else input("Enter the MySQL password: ")
    mysql_db_name = args.database if args.database else input("Enter the name of the MySQL database: ")
    
    return sqlite_db_path, mysql_server, mysql_username, mysql_password, mysql_db_name

def connect_sqlite(db_path):
    try:
        conn = sqlite3.connect(db_path)
        print("Successfully connected to SQLite")
        return conn
    except Exception as e:
        print(f"Failed to connect to SQLite: {e}")
        return None

def connect_mysql(server, username, password, db_name):
    try:
        conn = pymysql.connect(host=server, user=username, password=password, database=db_name)
        print("Successfully connected to MySQL")
        return conn
    except Exception as e:
        print(f"Failed to connect to MySQL: {e}")
        return None

def check_mysql_db(mysql_conn, db_name):
    cursor = mysql_conn.cursor()
    cursor.execute("SHOW DATABASES")
    
    databases = [db[0] for db in cursor.fetchall()]
    
    if db_name in databases:
        action = input(f"Database {db_name} already exists. Would you like to 'Replace' or 'Append'? ").lower()
        if action == 'replace':
            cursor.execute(f"DROP DATABASE {db_name}")
            cursor.execute(f"CREATE DATABASE {db_name}")
        elif action != 'append':
            print("Invalid option. Exiting.")
            exit(1)

def transfer_data(sqlite_conn, mysql_conn):
    print("Data transfer logic will go here.")

def main():
    parser = argparse.ArgumentParser(description='SQLite to MySQL Converter')
    parser.add_argument('--sqlite', help='Path to the SQLite database file')
    parser.add_argument('--server', help='MySQL server address')
    parser.add_argument('--username', help='MySQL username')
    parser.add_argument('--password', help='MySQL password')
    parser.add_argument('--database', help='MySQL database name')
    
    args = parser.parse_args()
    
    sqlite_db_path, mysql_server, mysql_username, mysql_password, mysql_db_name = get_user_inputs(args)
    
    print("Welcome to the SQLite to MySQL Converter!")
    
    # Establish database connections
    sqlite_conn = connect_sqlite(sqlite_db_path)
    mysql_conn = connect_mysql(mysql_server, mysql_username, mysql_password, mysql_db_name)
    
    if sqlite_conn:
        if mysql_conn:
            pass
        else:
            print(f"Unable to open the mysql database - Server: {mysql_server}, Username: {mysql_username}, Database: {mysql_db_name}")
    else:
        print(f"Unable to open the sqllite database {sqlite_db_path}")
    # Check and handle existing MySQL database
    # Transfer data
    # Close connections

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
