import sqlite3
import json

# Define the name of the database file
DB_NAME = 'certiscan.db'
# Define the name of your existing JSON file
JSON_FILE = 'trusted_issuers.json'

def create_database():
    """Creates the SQLite database and the trusted_issuers table."""
    conn = None # Initialize conn to None
    try:
        # Connect to SQLite - this will create the file if it doesn't exist
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Create the trusted_issuers table
        # We add 'UNIQUE' to issuer_name to prevent duplicates
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trusted_issuers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                issuer_name TEXT NOT NULL UNIQUE,
                verification_url TEXT  -- Optional: URL for manual verification
            )
        ''')

        print(f"Database '{DB_NAME}' created successfully.")
        print("Table 'trusted_issuers' created successfully or already exists.")

        # Commit the changes (important!)
        conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection if it was opened
        if conn:
            conn.close()

def populate_from_json():
    """Reads issuers from the JSON file and inserts them into the database."""
    conn = None # Initialize conn to None
    try:
        # Load data from the JSON file
        with open(JSON_FILE, 'r') as f:
            data = json.load(f)
            issuers = data.get('trusted', [])

        if not issuers:
            print(f"No issuers found in {JSON_FILE}. Skipping population.")
            return

        # Connect to the database
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        insert_count = 0
        skip_count = 0
        
        # Insert each issuer into the table
        # Use INSERT OR IGNORE to skip duplicates if the script is run multiple times
        for issuer in issuers:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO trusted_issuers (issuer_name) VALUES (?)
                ''', (issuer,))
                if cursor.rowcount > 0: # Checks if a row was actually inserted
                   insert_count += 1
                else:
                   skip_count +=1 
            except sqlite3.Error as e:
                print(f"Error inserting '{issuer}': {e}")
                skip_count += 1

        # Commit the changes
        conn.commit()
        print(f"Successfully inserted {insert_count} new issuers.")
        if skip_count > 0:
            print(f"Skipped {skip_count} duplicate or invalid issuers.")


    except FileNotFoundError:
        print(f"Error: {JSON_FILE} not found. Cannot populate database.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {JSON_FILE}.")
    except sqlite3.Error as e:
        print(f"An SQLite error occurred during population: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_database()
    populate_from_json()
    print("\nDatabase setup complete.")