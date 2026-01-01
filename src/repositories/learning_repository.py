import sqlite3
from typing import Optional

from src.db.constants import DATABASE_NAME


def create(
    project_id: Optional[int], challenge: str, solution: str, learning_type: str
):
    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            connection.row_factory = sqlite3.Row

            cursor = connection.cursor()

            create_learning_query = """
                INSERT INTO Learning (challenge, solution, learning_type, project_id)
                VALUES (?, ?, ?, ?)
            """

            cursor.execute(
                create_learning_query, (challenge, solution, learning_type, project_id)
            )

            connection.commit()

            print("Record inserted successfully")
    except Exception as e:
        print(f"Unknown error: {e}")
        raise
