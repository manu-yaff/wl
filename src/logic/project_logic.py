from textwrap import dedent

import click
from rich.console import Console
from rich.table import Table

from src.logic.project_exceptions import (
    EmptyUserInput,
    InvalidProjectContext,
    InvalidProjectName,
    ProjectDoesNotExists,
)
from src.repositories import project_repository
from src.utils import parse_user_input


def create():
    create_project_template = dedent(
        """\
        Name:

        ---

        Context:
        """
    )

    user_input = click.edit(text=create_project_template)

    if user_input is None:
        raise EmptyUserInput()

    keys_to_extract = ("name", "context")

    project_input = parse_user_input(user_input, keys_to_extract)

    if "name" not in project_input or project_input["name"] == "":
        raise InvalidProjectName()

    if "context" not in project_input or project_input["context"] == "":
        raise InvalidProjectContext()

    name, context = project_input.values()
    project_repository.create(name, context)


def update(id: int):
    if not (project := project_repository.get(id)):
        raise ProjectDoesNotExists()

    name = project["name"]
    context = project["context"]

    update_project_template = dedent(
        f"""\
        Name:
        {name}

        ---

        Context:
        {context}
        """
    )

    if (user_input := click.edit(text=update_project_template)) is None:
        raise EmptyUserInput()

    project_input = parse_user_input(user_input, ("name", "context"))

    if "name" not in project_input or project_input["name"] == "":
        raise InvalidProjectName()

    if "name" not in project_input or project_input["context"] == "":
        raise InvalidProjectContext()

    updated_name = project_input["name"]
    updated_context = project_input["context"]

    project_repository.update(id, updated_name, updated_context)


def read():
    projects = project_repository.read()

    table = Table("Id", "Project", "Context", "Date created")
    console = Console()

    for project in projects:
        id, name, context, created_at = (
            project["id"],
            project["name"],
            project["context"],
            project["created_at"],
        )

        table.add_row(str(id), name, context, created_at)

    console.print(table)
