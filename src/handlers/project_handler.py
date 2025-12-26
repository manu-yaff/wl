from src.app import app
from src.logic import project_logic


@app.command()
def create():
    project_logic.create()
