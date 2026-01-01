import typer

from src.handlers import learning_handler, project_handler

app = typer.Typer()
app.add_typer(project_handler.app, name="projects")
app.add_typer(learning_handler.app, name="learnings")

if __name__ == "__main__":
    app()
