from typing import Optional

import typer

from src.logic import learning_logic

app = typer.Typer()


@app.command()
def create(project_id: Optional[int] = None):
    learning_logic.create(project_id)
