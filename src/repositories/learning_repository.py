import sqlite3
from typing import Any, Optional

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


def get(id: int) -> Any | None:
    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            connection.row_factory = sqlite3.Row

            cursor = connection.cursor()

            get_learning_query = """
                SELECT * FROM Learning
                WHERE id = ?
            """

            cursor.execute(get_learning_query, (id,))

            return cursor.fetchone()

    except Exception as e:
        print(f"Unknown error: {e}")


def update(
    id: int,
    project_id: Optional[int],
    challenge: str,
    solution: str,
    learning_type: str,
) -> Any | None:
    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            connection.row_factory = sqlite3.Row

            cursor = connection.cursor()

            update_learning_query = """
                UPDATE Learning
                SET project_id = ?, challenge = ?, solution = ?, learning_type = ?
                WHERE id = ?
            """

            cursor.execute(
                update_learning_query,
                (project_id, challenge, solution, learning_type, id),
            )

            connection.commit()

            print("Record updated successfully")
    except Exception as e:
        print(f"Error: {e}")
        raise


def read() -> list:
    try:
        with sqlite3.connect(DATABASE_NAME) as connection:
            connection.row_factory = sqlite3.Row

            cursor = connection.cursor()

            read_learnings_query = """SELECT * FROM Learning"""

            cursor.execute(read_learnings_query)

            print("Read records successfully")

            return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        raise e
