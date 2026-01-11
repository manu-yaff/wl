from textwrap import dedent

import click
from rich.console import Console
from rich.table import Table

from src.logic.learning_exceptions import (
    InvalidChallenge,
    InvalidLearningType,
    InvalidSolution,
    LearningNotFound,
)
from src.repositories import learning_repository
from src.utils import Id, parse_user_input


def create():
    create_learning_template = dedent(
        """\
        Challenge:

        ---

        Solution:

        ---

        Type:

        ---
        Project id:
        """
    )
    keys_to_extract = ("challenge", "solution", "type", "project_id")

    if (user_input := click.edit(create_learning_template)) is None:
        raise Exception("Invalid user input")

    learning_input = parse_user_input(user_input, keys_to_extract)

    if "challenge" not in learning_input or learning_input["challenge"] == "":
        raise InvalidChallenge()

    if "solution" not in learning_input or learning_input["solution"] == "":
        raise InvalidSolution()

    if (
        not learning_input.get("type")
        or learning_input.get("type") != "soft"
        and learning_input.get("type") != "hard"
    ):
        raise InvalidLearningType()

    if (
        learning_input.get("project_id") is not None
        and learning_input.get("project_id") != ""
    ):
        value = learning_input.get("project_id")
        Id.validate(value)

    learning_repository.create(
        int(learning_input["project_id"]) if learning_input["project_id"] else None,
        learning_input["challenge"],
        learning_input["solution"],
        learning_input["type"],
    )


def update(id: int):
    if (learning := learning_repository.get(id)) is None:
        raise LearningNotFound()

    challenge = learning["challenge"]
    solution = learning["solution"]
    learning_type = learning["learning_type"]
    project_id = learning["project_id"]

    create_learning_template = dedent(
        f"""\
        Challenge:
        {challenge}

        ---

        Solution:
        {solution}

        ---

        Type:
        {learning_type}

        ---
        Project id:
        {project_id}
        """
    )

    keys_to_extract = ("challenge", "solution", "type", "project_id")

    if (user_input := click.edit(create_learning_template)) is None:
        raise Exception("Invalid user input")

    learning_input = parse_user_input(user_input, keys_to_extract)

    if not learning_input.get("challenge"):
        raise InvalidChallenge()

    if not learning_input.get("solution"):
        raise InvalidSolution()

    if (
        not learning_input.get("type")
        or learning_input.get("type") != "soft"
        and learning_input.get("type") != "hard"
    ):
        raise InvalidLearningType()

    if (
        learning_input.get("project_id") is not None
        and learning_input.get("project_id") != ""
    ):
        value = learning_input.get("project_id")
        Id.validate(value)

    updated_challenge = learning_input["challenge"]
    updated_solution = learning_input["solution"]
    updated_type = learning_input["type"]
    updated_project_id = learning_input["project_id"]

    learning_repository.update(
        id,
        int(updated_project_id) if updated_project_id else None,
        updated_challenge,
        updated_solution,
        updated_type,
    )


def read():
    console = Console()
    table = Table(
        "Id", "Challenge", "Solution", "Learing Type", "Project id", "Date created"
    )

    if not (learnings := learning_repository.read()):
        console.print("There are no learnings")

    for learning in learnings:
        id, challenge, solution, learning_type, project_id, created_at = (
            learning["id"],
            learning["challenge"],
            learning["solution"],
            learning["learning_type"],
            learning["project_id"],
            learning["created_at"],
        )

        table.add_row(
            str(id),
            challenge,
            solution,
            learning_type,
            str(project_id) if project_id else "None",
            created_at,
        )

    console.print(table)
