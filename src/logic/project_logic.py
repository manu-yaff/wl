from textwrap import dedent

import click

from src.logic.project_exceptions import (
    EmptyUserInput,
    InvalidProjectContext,
    InvalidProjectName,
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

    project_input = parse_user_input(user_input)

    if "Name" not in project_input or project_input["Name"] == "":
        raise InvalidProjectName()

    if "Context" not in project_input or project_input["Context"] == "":
        raise InvalidProjectContext()

    name, context = project_input.values()
    project_repository.create(name, context)
