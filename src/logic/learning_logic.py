from enum import Enum
from textwrap import dedent
from typing import Optional

import click

from src.repositories import learning_repository
from src.utils import parse_user_input


class InvalidChallenge(Exception):
    pass


class InvalidSolution(Exception):
    pass


class InvalidLearningType(Exception):
    pass


class LearningType(Enum):
    @staticmethod
    def contains(value):
        try:
            LearningType(value.lower())
            return True
        except Exception:
            return False

    soft = "soft"
    hard = "hard"


def create(project_id: Optional[int]):
    create_learning_template = dedent(
        """\
        Challenge:

        ---

        Solution:

        ---

        Type:
        """
    )
    keys_to_extract = ("challenge", "solution", "type")

    if (user_input := click.edit(create_learning_template)) is None:
        raise Exception("Invalid user input")

    learning_input = parse_user_input(user_input, keys_to_extract)

    if "challenge" not in learning_input or learning_input["challenge"] == "":
        raise InvalidChallenge()

    if "solution" not in learning_input or learning_input["solution"] == "":
        raise InvalidSolution()

    if (
        "type" not in learning_input
        or learning_input["type"] == ""
        or (
            LearningType.soft.value != learning_input["type"]
            and LearningType.hard.value != learning_input["type"]
        )
    ):
        raise InvalidLearningType()

    learning_repository.create(
        project_id,
        learning_input["challenge"],
        learning_input["solution"],
        learning_input["type"],
    )
