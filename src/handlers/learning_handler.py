import typer

from src.logic import learning_logic

app = typer.Typer()


@app.command()
def create():
    learning_logic.create()


@app.command()
def update(learning_id: int):
    learning_logic.update(learning_id)
