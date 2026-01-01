import typer

from src.logic import project_logic

app = typer.Typer()


@app.command()
def create():
    project_logic.create()


@app.command()
def update(id: int):
    project_logic.update(id)


@app.command()
def read():
    """
    Lists all projects
    """
    project_logic.read()
