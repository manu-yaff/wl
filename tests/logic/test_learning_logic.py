import sqlite3
from textwrap import dedent

import pytest
from faker import Faker
from pytest_mock import MockerFixture

from src.logic import learning_logic
from src.logic.learning_exceptions import (
    InvalidChallenge,
    InvalidLearningType,
    InvalidSolution,
    LearningNotFound,
)
from src.utils import InvalidId


def test_create_learning_fails_when_challenge_is_empty(
    mocker: MockerFixture, faker: Faker
):
    project_id = faker.random_int()
    mock_learning_repo = mocker.patch("src.logic.learning_logic.learning_repository")
    mock_click_edit = mocker.patch("src.logic.learning_logic.click")
    mock_click_edit.edit.return_value = dedent(
        """
        Challenge:
        ---
        Solution:
        update env var in config file
        ---
        Type:
        soft
        """
    )

    with pytest.raises(InvalidChallenge):
        learning_logic.create(project_id)

    mock_learning_repo.assert_not_called()


def test_create_learning_fails_when_challenge_is_missing(
    mocker: MockerFixture, faker: Faker
):
    project_id = faker.random_int()
    mock_learning_repo = mocker.patch("src.logic.learning_logic.learning_repository")
    mock_click_edit = mocker.patch("src.logic.learning_logic.click")
    mock_click_edit.edit.return_value = dedent(
        """
        ---
        Solution:
        update env var in config file
        ---
        Type:
        soft
        """
    )

    with pytest.raises(InvalidChallenge):
        learning_logic.create(project_id)

    mock_learning_repo.assert_not_called()


def test_create_learning_fails_when_solution_is_empty(
    mocker: MockerFixture, faker: Faker
):
    project_id = faker.random_int()
    mock_learning_repo = mocker.patch("src.logic.learning_logic.learning_repository")
    mock_click_edit = mocker.patch("src.logic.learning_logic.click")
    mock_click_edit.edit.return_value = dedent(
        """
        Challenge:
        Error while compiling code
        ---
        Solution:
        ---
        Type:
        soft
        """
    )

    with pytest.raises(InvalidSolution):
        learning_logic.create(project_id)

    mock_learning_repo.assert_not_called()


def test_create_learning_fails_when_solution_is_missing(
    mocker: MockerFixture, faker: Faker
):
    project_id = faker.random_int()
    mock_learning_repo = mocker.patch("src.logic.learning_logic.learning_repository")
    mock_click_edit = mocker.patch("src.logic.learning_logic.click")
    mock_click_edit.edit.return_value = dedent(
        """
        Challenge:
        Error while compiling code
        ---
        Type:
        soft
        """
    )

    with pytest.raises(InvalidSolution):
        learning_logic.create(project_id)

    mock_learning_repo.assert_not_called()


def test_create_learning_fails_when_learning_type_is_empty(
    mocker: MockerFixture, faker: Faker
):
    project_id = faker.random_int()
    mock_learning_repo = mocker.patch("src.logic.learning_logic.learning_repository")
    mock_click_edit = mocker.patch("src.logic.learning_logic.click")
    mock_click_edit.edit.return_value = dedent(
        """\
        Challenge:
        Error while compiling code
        ---
        Solution:
        update env var from config file
        ---
        Type:
        """
    )

    with pytest.raises(InvalidLearningType):
        learning_logic.create(project_id)

    mock_learning_repo.assert_not_called()


def test_create_learning_fails_when_learning_type_is_missing(
    mocker: MockerFixture, faker: Faker
):
    project_id = faker.random_int()
    mock_learning_repo = mocker.patch("src.logic.learning_logic.learning_repository")
    mock_click_edit = mocker.patch("src.logic.learning_logic.click")
    mock_click_edit.edit.return_value = dedent(
        """\
        Challenge:
        Error while compiling code
        ---
        Solution:
        update env var from config file
        ---
        Type:
        """
    )

    with pytest.raises(InvalidLearningType):
        learning_logic.create(project_id)

    mock_learning_repo.assert_not_called()


def test_create_learning_fails_when_learning_type_is_not_allowed(
    mocker: MockerFixture, faker: Faker
):
    project_id = faker.random_int()
    mock_learning_repo = mocker.patch("src.logic.learning_logic.learning_repository")
    mock_click_edit = mocker.patch("src.logic.learning_logic.click")
    mock_click_edit.edit.return_value = dedent(
        """\
        Challenge:
        Error while compiling code
        ---
        Solution:
        update env var from config file
        ---
        Type:
        personal
        """
    )

    with pytest.raises(InvalidLearningType):
        learning_logic.create(project_id)

    mock_learning_repo.assert_not_called()


def test_create_learning_fails_when_data_base_insertion_fails(
    mocker: MockerFixture, faker: Faker
):
    project_id = faker.random_int()
    mock_learning_repo = mocker.patch("src.logic.learning_logic.learning_repository")
    mock_click_edit = mocker.patch("src.logic.learning_logic.click")
    mock_click_edit.edit.return_value = dedent(
        """\
        Challenge:
        Error while compiling code
        ---
        Solution:
        update env var from config file
        ---
        Type:
        soft
        """
    )
    mock_learning_repo.create.side_effect = sqlite3.IntegrityError()

    with pytest.raises(sqlite3.IntegrityError):
        learning_logic.create(project_id)

    mock_learning_repo.assert_not_called()


def test_create_learning_successfully_saves_in_db(mocker: MockerFixture, faker: Faker):
    project_id = faker.random_int()
    mock_learning_repo = mocker.patch("src.logic.learning_logic.learning_repository")
    mock_click_edit = mocker.patch("src.logic.learning_logic.click")
    mock_click_edit.edit.return_value = dedent(
        """\
        Challenge:
        Error while compiling code
        ---
        Solution:
        update env var from config file
        ---
        Type:
        soft
        """
    )

    learning_logic.create(project_id)

    mock_learning_repo.create.assert_called_with(
        project_id,
        "Error while compiling code",
        "update env var from config file",
        "soft",
    )


class TestUpdateLearning:
    def test_update_learning_fails_when_learning_not_found(
        self, mocker: MockerFixture, faker: Faker
    ):
        learning_id = faker.random_int()
        mock_learning_repo = mocker.patch(
            "src.logic.learning_logic.learning_repository"
        )
        mock_learning_repo.get.return_value = None
        mock_click_edit = mocker.patch("src.logic.learning_logic.click")
        mock_click_edit.edit.return_value = dedent(
            """
            Challenge:
            ---
            Solution:
            update env var in config file
            ---
            Type:
            soft
            """
        )

        with pytest.raises(LearningNotFound):
            learning_logic.update(learning_id)

        mock_learning_repo.assert_not_called()

    def test_update_learning_fails_when_challenge_is_empty(
        self, mocker: MockerFixture, faker: Faker
    ):
        learning_id = faker.random_int()
        mock_learning_repo = mocker.patch(
            "src.logic.learning_logic.learning_repository"
        )
        mock_click_edit = mocker.patch("src.logic.learning_logic.click")
        mock_click_edit.edit.return_value = dedent(
            """
            Challenge:
            ---
            Solution:
            update env var in config file
            ---
            Type:
            soft
            """
        )

        with pytest.raises(InvalidChallenge):
            learning_logic.update(learning_id)

        mock_learning_repo.assert_not_called()

    def test_update_learning_fails_challenge_is_missing(
        self, mocker: MockerFixture, faker: Faker
    ):
        learning_id = faker.random_int()
        mock_learning_repo = mocker.patch(
            "src.logic.learning_logic.learning_repository"
        )
        mock_click_edit = mocker.patch("src.logic.learning_logic.click")
        mock_click_edit.edit.return_value = dedent(
            """
            Solution:
            update env var in config file
            ---
            Type:
            soft
            """
        )

        with pytest.raises(InvalidChallenge):
            learning_logic.update(learning_id)

        mock_learning_repo.assert_not_called()

    def test_update_learning_fails_solution_is_empty(
        self, mocker: MockerFixture, faker: Faker
    ):
        learning_id = faker.random_int()
        mock_learning_repo = mocker.patch(
            "src.logic.learning_logic.learning_repository"
        )
        mock_click_edit = mocker.patch("src.logic.learning_logic.click")
        mock_click_edit.edit.return_value = dedent(
            """
            Challenge:
            this is a challenge
            Solution:
            ---
            Type:
            soft
            """
        )

        with pytest.raises(InvalidSolution):
            learning_logic.update(learning_id)

        mock_learning_repo.assert_not_called()

    def test_update_learning_fails_solution_missing(
        self, mocker: MockerFixture, faker: Faker
    ):
        learning_id = faker.random_int()
        mock_learning_repo = mocker.patch(
            "src.logic.learning_logic.learning_repository"
        )
        mock_click_edit = mocker.patch("src.logic.learning_logic.click")
        mock_click_edit.edit.return_value = dedent(
            """
            Challenge:
            this is a challenge
            
            ---
            Type:
            soft
            """
        )

        with pytest.raises(InvalidSolution):
            learning_logic.update(learning_id)

        mock_learning_repo.assert_not_called()

    def test_update_learning_fails_when_learning_type_is_empty(
        self, mocker: MockerFixture, faker: Faker
    ):
        learning_id = faker.random_int()
        mock_learning_repo = mocker.patch(
            "src.logic.learning_logic.learning_repository"
        )
        mock_click_edit = mocker.patch("src.logic.learning_logic.click")
        mock_click_edit.edit.return_value = dedent(
            """
            Challenge:
            this is a challenge
            
            ---
            Solution:
            this is a solution

            ---
            Type:
            
            """
        )

        with pytest.raises(InvalidLearningType):
            learning_logic.update(learning_id)

        mock_learning_repo.assert_not_called()

    def test_update_learning_fails_when_learning_type_is_missing(
        self, mocker: MockerFixture, faker: Faker
    ):
        learning_id = faker.random_int()
        mock_learning_repo = mocker.patch(
            "src.logic.learning_logic.learning_repository"
        )
        mock_click_edit = mocker.patch("src.logic.learning_logic.click")
        mock_click_edit.edit.return_value = dedent(
            """
            Challenge:
            this is a challenge
            
            ---
            Solution:
            this is a solution

            ---
            """
        )

        with pytest.raises(InvalidLearningType):
            learning_logic.update(learning_id)

        mock_learning_repo.assert_not_called()

    def test_update_learning_fails_when_learning_type_is_not_allowed(
        self, mocker: MockerFixture, faker: Faker
    ):
        learning_id = faker.random_int()
        mock_learning_repo = mocker.patch(
            "src.logic.learning_logic.learning_repository"
        )
        mock_click_edit = mocker.patch("src.logic.learning_logic.click")
        mock_click_edit.edit.return_value = dedent(
            """
            Challenge:
            this is a challenge
            
            ---
            Solution:
            this is a solution

            ---
            Type:
            personal
            """
        )

        with pytest.raises(InvalidLearningType):
            learning_logic.update(learning_id)

        mock_learning_repo.assert_not_called()

    def test_update_learning_fails_when_data_base_insertion_fails(
        self, mocker: MockerFixture, faker: Faker
    ):
        learning_id = faker.random_int()
        mock_learning_repo = mocker.patch(
            "src.logic.learning_logic.learning_repository"
        )
        mock_learning_repo.update.side_effect = sqlite3.IntegrityError()
        mock_click_edit = mocker.patch("src.logic.learning_logic.click")
        mock_click_edit.edit.return_value = dedent(
            """
            Challenge:
            this is a challenge
            
            ---
            Solution:
            this is a solution

            ---
            Type:
            soft
            """
        )

        with pytest.raises(sqlite3.IntegrityError):
            learning_logic.update(learning_id)

        mock_learning_repo.assert_not_called()

    def test_update_learning_fails_when_project_id_is_not_number(
        self, mocker: MockerFixture, faker: Faker
    ):
        learning_id = faker.random_int()
        mock_learning_repo = mocker.patch(
            "src.logic.learning_logic.learning_repository"
        )
        mock_click_edit = mocker.patch("src.logic.learning_logic.click")
        mock_click_edit.edit.return_value = dedent(
            """
            Challenge:
            this is a challenge
            
            ---
            Solution:
            this is a solution

            ---
            Type:
            soft

            ---
            Project id:
            hello
            """
        )

        with pytest.raises(InvalidId):
            learning_logic.update(learning_id)

        mock_learning_repo.assert_not_called()

    def test_update_learning_successfully_saves_when_project_id_is_missing(
        self, mocker: MockerFixture, faker: Faker
    ):
        learning_id = faker.random_int()
        mock_learning_repo = mocker.patch(
            "src.logic.learning_logic.learning_repository"
        )
        mock_click_edit = mocker.patch("src.logic.learning_logic.click")
        mock_click_edit.edit.return_value = dedent(
            """
            Challenge:
            this is a challenge
            
            ---
            Solution:
            this is a solution

            ---
            Type:
            soft
            """
        )

        learning_logic.update(learning_id)

        mock_learning_repo.update.assert_called_once()

    def test_update_learning_successfully_saves_when_project_id_is_empty(
        self, mocker: MockerFixture, faker: Faker
    ):
        learning_id = faker.random_int()
        mock_learning_repo = mocker.patch(
            "src.logic.learning_logic.learning_repository"
        )
        mock_click_edit = mocker.patch("src.logic.learning_logic.click")
        mock_click_edit.edit.return_value = dedent(
            """
            Challenge:
            this is a challenge
            
            ---
            Solution:
            this is a solution

            ---
            Type:
            soft

            ---
            Project id:
            """
        )

        learning_logic.update(learning_id)

        mock_learning_repo.update.assert_called_once()

    def test_update_learning_successfully_saves_in_db(
        self, mocker: MockerFixture, faker: Faker
    ):
        learning_id = faker.random_int()
        mock_learning_repo = mocker.patch(
            "src.logic.learning_logic.learning_repository"
        )
        mock_click_edit = mocker.patch("src.logic.learning_logic.click")
        mock_click_edit.edit.return_value = dedent(
            """
            Challenge:
            this is a challenge
            
            ---
            Solution:
            this is a solution

            ---
            Type:
            soft

            ---
            Project id:
            12
            """
        )

        learning_logic.update(learning_id)

        mock_learning_repo.update.assert_called_once()
