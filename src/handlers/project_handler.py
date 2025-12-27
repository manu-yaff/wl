from src.app import app
from src.logic import project_logic


@app.command()
def create():
    project_logic.create()


@app.command()
def update(id: int):
    project_logic.update(id)
