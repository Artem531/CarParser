import sqlite3
from config import get_params, get_car_brands
from main import generate_db_name

def create_table(connection, create_table_sql):
    """ Helper function to create a table from the create_table_sql statement """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_sql)
    except Exception as e:
        print(f"An error occurred: {e}")


def import_data(source_db, master_db_connection, table_name):
    try:
        # Connecting to the source database
        source_connection = sqlite3.connect(source_db)
        source_cursor = source_connection.cursor()

        # Query to fetch all data from a table
        source_cursor.execute(f"SELECT * FROM {table_name}")
        rows = source_cursor.fetchall()

        # Inserting data into the master database
        master_cursor = master_db_connection.cursor()
        if table_name == "sold_cars":
            master_cursor.executemany(
                f"INSERT OR IGNORE INTO {table_name} (url, city, price, details, insert_time) VALUES (?,?,?,?,?)", rows)
        else:
            master_cursor.executemany(f"INSERT OR IGNORE INTO {table_name} VALUES (?,?,?,?,?,?)", rows)

        # Commit the transaction and report the number of rows added
        master_db_connection.commit()
        print(f"Added {master_cursor.rowcount} new rows to {table_name} from {source_db}")

        source_connection.close()
    except Exception as e:
        print(f"An error occurred while importing data from {source_db}: {e}")


def main():
    master_db_path = "../master_database.db"  # Path to your master database
    source_dbs = []  # List of your source database paths

    params = get_params(brand="")
    for car_brand in get_car_brands():
        params['brand'] = car_brand[1].split(":")[-1]
        db_name = generate_db_name(params)
        source_dbs.append(db_name)

    # Connect to the master database
    master_connection = sqlite3.connect(master_db_path)

    # SQL statements to create tables
    create_cars_DB = '''CREATE TABLE IF NOT EXISTS cars
                (url TEXT PRIMARY KEY, city TEXT, price TEXT, details TEXT, session_updated INTEGER DEFAULT 0,
                insert_time DATETIME DEFAULT (datetime('now', 'localtime')))'''

    create_sold_cars_DB = '''CREATE TABLE IF NOT EXISTS sold_cars
                (url TEXT PRIMARY KEY, city TEXT, price TEXT, details TEXT,
                insert_time DATETIME DEFAULT (datetime('now', 'localtime')))'''

    # Create tables in the master database
    create_table(master_connection, create_cars_DB)
    create_table(master_connection, create_sold_cars_DB)

    # Import data from each source database
    for db in source_dbs:
        import_data(db, master_connection, "cars")
        import_data(db, master_connection, "sold_cars")

    master_connection.close()


if __name__ == "__main__":
    main()
