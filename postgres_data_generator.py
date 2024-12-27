import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import random
import string

# Configuration
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"

ROWS_PER_TABLE = 268435  # Adjust based on target size
DATABASE_COUNT = 50
TABLES_PER_DATABASE = 5
DB_NAME_PREFIX = "test_db_"
TABLE_NAME_PREFIX = "table_"

# Database connection to the default database
connection = psycopg2.connect(
    dbname="postgres",
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT
)
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()

# Helper functions
def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def create_database(db_name):
    try:
        cursor.execute(f"CREATE DATABASE {db_name};")
        print(f"Database {db_name} created successfully.")
    except Exception as e:
        print(f"Error creating database {db_name}: {e}")

def create_table_and_insert_data(db_name):
    try:
        # Connect to the new database
        db_connection = psycopg2.connect(
            dbname=db_name,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )
        db_cursor = db_connection.cursor()

        # Create tables and insert data
        for table_num in range(1, TABLES_PER_DATABASE + 1):  # Create 5 tables per database
            table_name = f"{TABLE_NAME_PREFIX}{table_num}"
            db_cursor.execute(f"""
                CREATE TABLE {table_name} (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50),
                    value INTEGER
                );
            """)

            # Insert random data into the table
            for _ in range(ROWS_PER_TABLE):  # Insert ROWS_PER_TABLE rows per table
                name = random_string()
                value = random.randint(1, 10000)
                db_cursor.execute(
                    f"INSERT INTO {table_name} (name, value) VALUES (%s, %s);",
                    (name, value)
                )

        db_connection.commit()
        db_cursor.close()
        db_connection.close()
        print(f"Tables and data created in database {db_name}.")

    except Exception as e:
        print(f"Error in database {db_name}: {e}")

# Main script to create databases and populate data
for db_num in range(1, DATABASE_COUNT + 1):  # Create DATABASE_COUNT databases
    db_name = f"{DB_NAME_PREFIX}{db_num}"
    create_database(db_name)
    create_table_and_insert_data(db_name)

# Cleanup
cursor.close()
connection.close()
print("Test data generation complete.")
