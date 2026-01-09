from typing import Optional

import typer

from src.logic import learning_logic

app = typer.Typer()


@app.command()
def create(project_id: Optional[int] = None):
    learning_logic.create(project_id)


@app.command()
def update(learning_id: int):
    learning_logic.update(learning_id)
