import click
from click import Context, Command

from modules.config.config import Config
from modules.project.project_model import ProjectType
from modules.project.project_service import ProjectService
from utils.file.file_processor import FileProcessor

file_service = FileProcessor()
project_service = ProjectService(Config.load().project)

@click.group
def project() -> Command:
    pass

@project.command()
@click.option('--path', default=None, help="Project path")
@click.option('--name', default=None, help="Project name")
@click.option('--type', type=click.Choice([e.value for e in ProjectType], case_sensitive=False), default=None, help="Project type")
@click.pass_context
def add(ctx: Context,  path: str | None, name: str | None, type: str | None):
    project = project_service.add_project(path, name, type)
    click.secho(f"Project created {project}", fg="green")
        # FIXME: Update the active path later
        #  self.update_project_path_config(project_id)

@project.command()
@click.pass_context
def show(ctx: Context):
    project_service.show_projects()


