import sqlite3

from src.db.constants import DATABASE_NAME

if __name__ == "__main__":
    with sqlite3.connect(DATABASE_NAME) as connection:
        cursor = connection.cursor()

        create_project_table_query = """
        CREATE TABLE IF NOT EXISTS Project (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            context TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        """

        cursor.execute(create_project_table_query)

        connection.commit()

        print('"Project" table created successfully')
