import sqlite3

from src.db.constants import DATABASE_NAME

if __name__ == "__main__":
    with sqlite3.connect(DATABASE_NAME) as connection:
        cursor = connection.cursor()

        create_project_table_query = """
        CREATE TABLE IF NOT EXISTS Learning (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            challenge TEXT NOT NULL,
            solution TEXT NOT NULL,
            learning_type TEXT NOT NULL CHECK(learning_type IN ('soft', 'hard')),
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT (datetime('now')),
            project_id INTEGER,
            FOREIGN KEY (project_id) REFERENCES Project(id)
        );
        """

        cursor.execute(create_project_table_query)

        connection.commit()

        print('"Learning" table created successfully')
