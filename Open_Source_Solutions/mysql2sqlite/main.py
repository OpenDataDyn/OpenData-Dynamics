import argparse
import sqlite3
import pymysql
import logging
import re

logging.basicConfig(filename='db_transfer.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

def sqlite_to_mysql_type(sqlite_type):
    type_mapping = {
        'INTEGER': 'INT',
        'REAL': 'FLOAT',
        'TEXT': 'TEXT',
        'BLOB': 'BLOB',
        'NUMERIC': 'DECIMAL(10, 5)',
        'BOOLEAN': 'TINYINT(1)',
        'DATETIME': 'DATETIME',
        'DATE': 'DATE',
        'TIME': 'TIME',
        'VARCHAR': 'VARCHAR(255)',
        'CHAR': 'CHAR(255)',
        'INT8': 'BIGINT',
        'BIGINT': 'BIGINT',
        'SMALLINT': 'SMALLINT',
        'FLOAT': 'FLOAT',
        'DOUBLE': 'DOUBLE',
        # Add more mappings as needed
    }
    return type_mapping.get(sqlite_type.upper(), 'TEXT')  # Default to TEXT

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
        logging.info(f"Successfully connected to SQLite database at {db_path}")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to SQLite: {e}")
        raise ConnectionError("Failed to connect to SQLite")  # Raise custom exception

def connect_mysql(server, username, password, db_name=None):
    try:
        conn = pymysql.connect(host=server, user=username, password=password, database=db_name)
        logging.info(f"Successfully connected to MySQL{' server' if db_name is None else f' database {db_name}'}")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to MySQL: {e}")
        raise ConnectionError(f"Failed to connect to MySQL: {e}")  # Raise an exception

def create_mysql_db_if_not_exists(conn, db_name):
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    databases = [db[0] for db in cursor.fetchall()]
    
    if db_name not in databases:
        cursor.execute(f"CREATE DATABASE {db_name}")
        logging.info(f"Database {db_name} created.")
    cursor.close()

def check_mysql_db(mysql_conn, db_name):
    cursor = None
    try:
        cursor = mysql_conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        
        if db_name in databases:
            action = input(f"Database {db_name} already exists. Would you like to 'Replace' or 'Append'? ").lower()
            if action == 'replace':
                cursor.execute(f"DROP DATABASE {db_name}")
                cursor.execute(f"CREATE DATABASE {db_name}")
                logging.info(f"Database {db_name} dropped and recreated.")
                return True  # Signal that the database was dropped and recreated
            elif action == 'append':
                logging.info(f"Appending to existing database {db_name}.")
                return False  # Signal that the database was not dropped
            else:
                logging.error("Invalid option. Exiting.")
                exit(1)
        else:
            cursor.execute(f"CREATE DATABASE {db_name}")
            logging.info(f"Database {db_name} not found. Created new database.")
            return False  # Signal that the database was not dropped
    except Exception as e:
        logging.error(f"An error occurred while checking/creating the MySQL database: {e}")
        return None
    finally:
        if cursor:
            cursor.close()  # Explicitly close the cursor


def extract_constraints_from_sqlite_schema(sqlite_schema, table_name):
    # Regex to match foreign key and check constraints in SQLite schema
    foreign_key_re = re.compile(r"FOREIGN KEY\s*\(.*\)\s*REFERENCES.*", re.IGNORECASE)
    check_re = re.compile(r"CHECK\s*\(.*\)", re.IGNORECASE)

    foreign_keys = foreign_key_re.findall(sqlite_schema)
    checks = check_re.findall(sqlite_schema)

    return foreign_keys, checks

def add_constraints_to_mysql_table(mysql_cursor, table_name, foreign_keys, checks):
    for fk in foreign_keys:
        alter_table_query = f"ALTER TABLE {table_name} ADD {fk}"
        mysql_cursor.execute(alter_table_query)
        logging.info(f"Added FOREIGN KEY constraint to table {table_name}")

    for check in checks:
        alter_table_query = f"ALTER TABLE {table_name} ADD {check}"
        mysql_cursor.execute(alter_table_query)
        logging.info(f"Added CHECK constraint to table {table_name}")

def transfer_data(sqlite_conn, mysql_conn):
    # Step 1: List all tables in SQLite database
    sqlite_cursor = sqlite_conn.cursor()
    sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = sqlite_cursor.fetchall()
    
    # Initialize MySQL cursor
    mysql_cursor = mysql_conn.cursor()
    
    # Dictionary to store user decisions for each table
    user_decisions = {}

    # First Loop: Check if tables exist in MySQL and gather user decisions
    for table in tables:
        table_name = table[0]
        
        # Check if table exists in MySQL
        mysql_cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = mysql_cursor.fetchone()
        
        # If table exists, ask for user action
        if result:
            while True:  # Loop for user input
                action = input(f"Table {table_name} already exists. Would you like to 'Replace' or 'Append'? ").lower()
                if action in ['replace', 'append']:
                    logging.info(f"User chose to '{action}' table {table_name}.")
                    user_decisions[table_name] = action
                    break  # Exit the loop if valid input
                else:
                    logging.warning("Invalid option. Please enter 'Replace' or 'Append'.")
    
    # Second Loop: Execute the user decisions and transfer data
    for table in tables:
        table_name = table[0]
        action = user_decisions.get(table_name, None)
        
        # Drop table if 'replace' action was chosen
        if action == 'replace':
            mysql_cursor.execute(f"DROP TABLE {table_name}")
            logging.info(f"Table {table_name} dropped.")
        
        # Create table if it's a new table or 'replace' action was chosen
        if action != 'append':
            sqlite_cursor.execute(f"PRAGMA table_info({table_name})")
            columns = sqlite_cursor.fetchall()
            create_table_query = f"CREATE TABLE {table_name} ("
            for column in columns:
                mysql_type = sqlite_to_mysql_type(column[2])
                create_table_query += f"{column[1]} {mysql_type}, "
            create_table_query = create_table_query[:-2] + ")"
            mysql_cursor.execute(create_table_query)
            logging.info(f"Table {table_name} created.")


            # Fetch and create indexes
            sqlite_cursor.execute(f"PRAGMA index_list({table_name})")
            index_list = sqlite_cursor.fetchall()
            for index in index_list:
                index_name = index[1]
                sqlite_cursor.execute(f"PRAGMA index_info({index_name})")
                index_columns = [col[2] for col in sqlite_cursor.fetchall()]
                index_columns_str = ",".join(index_columns)
                unique = "UNIQUE" if index[2] else ""
                create_index_query = f"CREATE {unique} INDEX {index_name} ON {table_name} ({index_columns_str})"
                mysql_cursor.execute(create_index_query)
                logging.info(f"Index {index_name} created.")

            # Fetch SQLite table schema
            sqlite_cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
            sqlite_schema = sqlite_cursor.fetchone()[0]

            # Extract constraints from SQLite schema
            foreign_keys, checks = extract_constraints_from_sqlite_schema(sqlite_schema, table_name)

            # Add constraints to MySQL table
            add_constraints_to_mysql_table(mysql_cursor, table_name, foreign_keys, checks)
        
        # Transfer Data
        sqlite_cursor.execute(f"SELECT * FROM {table_name}")
        rows = sqlite_cursor.fetchall()
        logging.info(f"Transferring {len(rows)} rows for table {table_name}.")
        for row in rows:
            values = ', '.join(['%s' for _ in row])
            insert_query = f"INSERT INTO {table_name} VALUES ({values})"
            try:
                mysql_cursor.execute(insert_query, row)
            except Exception as e:
                logging.error(f"Failed to execute query: {insert_query}. Error: {e}")
                raise  # Re-raise the caught exception
    
    # Commit and close connections
    mysql_conn.commit()
    mysql_cursor.close()
    sqlite_cursor.close()


def main():
    parser = argparse.ArgumentParser(description='SQLite to MySQL Converter')
    parser.add_argument('--sqlite', help='Path to the SQLite database file you want to convert.')
    parser.add_argument('--server', help='Address of the MySQL server to which you want to transfer the data.')
    parser.add_argument('--username', help='Username for the MySQL database.')
    parser.add_argument('--password', help='Password for the MySQL database.')
    parser.add_argument('--database', help='Name of the MySQL database where you want to transfer the data.')
    
    args = parser.parse_args()
    
    sqlite_db_path, mysql_server, mysql_username, mysql_password, mysql_db_name = get_user_inputs(args)
    
    print("Welcome to the SQLite to MySQL Converter!")
    
    sqlite_conn = None
    mysql_conn = None
    try:
        # Establish database connections
        sqlite_conn = connect_sqlite(sqlite_db_path)
        mysql_conn = connect_mysql(mysql_server, mysql_username, mysql_password)
        create_mysql_db_if_not_exists(mysql_conn, mysql_db_name)

        mysql_conn.close()
        mysql_conn = connect_mysql(mysql_server, mysql_username, mysql_password, mysql_db_name)
        
        # Check if MySQL database exists and reconnect if necessary
        was_dropped = check_mysql_db(mysql_conn, mysql_db_name)
        if was_dropped:
            mysql_conn.close()
            mysql_conn = connect_mysql(mysql_server, mysql_username, mysql_password, mysql_db_name)
        
        if mysql_conn and sqlite_conn:
            # Start a transaction
            mysql_conn.begin()
            transfer_data(sqlite_conn, mysql_conn)
            # Commit transaction
            mysql_conn.commit()
        elif not sqlite_conn:
            logging.error(f"Unable to open the SQLite database {sqlite_db_path}")
        else:
            logging.error(f"Unable to open the MySQL database - Server: {mysql_server}, Username: {mysql_username}, Database: {mysql_db_name}")
            
    except Exception as e:
        logging.exception(f"An error occurred: {e}")
        if mysql_conn:
            mysql_conn.rollback()
        
    finally:
        if sqlite_conn:
            sqlite_conn.close()
        if mysql_conn:
            mysql_conn.close()

if __name__ == "__main__":
    main()
