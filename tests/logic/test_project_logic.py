import sqlite3
from textwrap import dedent
from unittest import TestCase, mock

from faker import Faker
from pytest_mock import MockerFixture

from src.logic import project_logic
from src.logic.project_exceptions import (
    EmptyUserInput,
    InvalidProjectContext,
    InvalidProjectName,
    ProjectDoesNotExists,
)


class TestCreateProjectLogic(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.project_name = self.faker.catch_phrase()
        self.project_context = self.faker.paragraph()

    @mock.patch("src.logic.project_logic.click")
    @mock.patch("src.logic.project_logic.project_repository")
    def test_create_throw_exception_when_user_input_is_none(
        self, mock_project_repo, mock_click
    ):
        mock_click.edit.return_value = None

        with self.assertRaises(EmptyUserInput):
            project_logic.create()

        mock_project_repo.assert_not_called()

    @mock.patch("src.logic.project_logic.click")
    @mock.patch("src.logic.project_logic.project_repository")
    def test_create_throw_exception_when_name_is_none(
        self, mock_project_repo, mock_click
    ):
        mock_click.edit.return_value = dedent(
            f"""
            ---
            Context:
            {self.project_context}
            """
        )

        with self.assertRaises(InvalidProjectName):
            project_logic.create()

        mock_project_repo.assert_not_called()

    @mock.patch("src.logic.project_logic.click")
    @mock.patch("src.logic.project_logic.project_repository")
    def test_create_throw_exception_when_name_is_empty(
        self, mock_project_repo, mock_click
    ):
        mock_click.edit.return_value = dedent(
            f"""
            Name:
            ---
            Context:
            {self.project_context}
            """
        )

        with self.assertRaises(InvalidProjectName):
            project_logic.create()

        mock_project_repo.assert_not_called()

    @mock.patch("src.logic.project_logic.click")
    @mock.patch("src.logic.project_logic.project_repository")
    def test_create_throw_exception_when_context_is_none(
        self, mock_project_repo, mock_click
    ):
        mock_click.edit.return_value = dedent(
            f"""
            Name:
            {self.project_name}
            ---
            """
        )

        with self.assertRaises(InvalidProjectContext):
            project_logic.create()

        mock_project_repo.assert_not_called()

    @mock.patch("src.logic.project_logic.click")
    @mock.patch("src.logic.project_logic.project_repository")
    def test_create_throw_exception_when_context_is_empty(
        self, mock_project_repo, mock_click
    ):
        mock_click.edit.return_value = dedent(
            f"""
            Name:
            {self.project_name}
            ---
            Context:
            """
        )

        with self.assertRaises(InvalidProjectContext):
            project_logic.create()

        mock_project_repo.assert_not_called()

    @mock.patch("src.logic.project_logic.click")
    @mock.patch("src.logic.project_logic.project_repository")
    def test_create_throw_exception_when_name_already_exists(
        self, mock_project_repo, mock_click
    ):
        mock_project_repo.create.side_effect = sqlite3.IntegrityError()
        mock_click.edit.return_value = dedent(
            f"""
            Name:
            {self.project_name}
            ---
            Context:
            {self.project_context}
            """
        )

        with self.assertRaises(sqlite3.IntegrityError):
            project_logic.create()

    @mock.patch("src.logic.project_logic.click")
    @mock.patch("src.logic.project_logic.project_repository")
    def test_create_successfully_saves(self, mock_project_repo, mock_click):
        mock_click.edit.return_value = dedent(
            f"""
            Name:
            {self.project_name}
            ---
            Context:
            {self.project_context}
            """
        )

        project_logic.create()

        mock_project_repo.create.assert_called_with(
            self.project_name, self.project_context
        )


class TestUpdateProjectLogic(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.project_id = self.faker.random_int(min=1, max=100000)
        self.project_name = self.faker.catch_phrase()
        self.project_context = self.faker.paragraph()

    @mock.patch("src.logic.project_logic.project_repository")
    def test_update_project_does_not_exists(self, mock_project_repo):
        mock_project_repo.get.return_value = None

        with self.assertRaises(ProjectDoesNotExists):
            project_logic.update(self.project_id)

    @mock.patch("src.logic.project_logic.click")
    @mock.patch("src.logic.project_logic.project_repository")
    def test_update_successfully_saves(self, mock_project_repo, mock_click):
        mock_click.edit.return_value = dedent(
            f"""
            Name:
            {self.project_name}
            ---
            Context:
            {self.project_context}
            """
        )

        project_logic.update(self.project_id)

        mock_project_repo.update.assert_called_with(
            self.project_id, self.project_name, self.project_context
        )

    @mock.patch("src.logic.project_logic.click")
    @mock.patch("src.logic.project_logic.project_repository")
    def test_update_project_name_already_exists(self, mock_project_repo, mock_click):
        mock_project_repo.update.side_effect = sqlite3.IntegrityError()
        mock_click.edit.return_value = dedent(
            f"""
            Name:
            {self.project_name}
            ---
            Context:
            {self.project_context}
            """
        )

        with self.assertRaises(sqlite3.IntegrityError):
            project_logic.update(self.project_id)


def test_list_projects_returns_empty_list_when_there_are_no_projects(
    mocker: MockerFixture,
):
    mock_project_repo = mocker.patch("src.logic.project_logic.project_repository")
    mock_console_print = mocker.patch("src.logic.project_logic.Console.print")
    mock_project_repo.read.return_value = []

    project_logic.read()

    mock_console_print.assert_called_once()


def test_list_projects_shows_projects_with_properties(
    mocker: MockerFixture, faker: Faker
):
    mocker.patch("src.logic.project_logic.Table.add_row")
    mock_console_print = mocker.patch("src.logic.project_logic.Console.print")
    mock_project_repo = mocker.patch("src.logic.project_logic.project_repository")
    projects = [
        {
            "id": faker.random_int(),
            "name": faker.catch_phrase(),
            "context": faker.paragraph(),
            "created_at": faker.date_time(),
        }
    ]
    mock_project_repo.read.return_value = projects

    project_logic.read()

    mock_console_print.assert_called_once()
