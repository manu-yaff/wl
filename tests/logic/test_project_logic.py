import sqlite3
from textwrap import dedent
from unittest import TestCase, mock

from faker import Faker

from src.logic import project_logic
from src.logic.project_exceptions import (
    EmptyUserInput,
    InvalidProjectContext,
    InvalidProjectName,
)


class TestCreateProjectLogic(TestCase):
    def setUp(self) -> None:
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
