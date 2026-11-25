import click
from click import Context
from modules.project.project_model import ProjectType
from utils.file.file_processor import FileProcessor

file_service = FileProcessor()

@click.Group
def project():
    pass

@project.command()
@click.option('--path', default=None, help="Project path")
@click.option('--name', default=None, help="Project name")
@click.option('--type', type=click.Choice([e.value for e in ProjectType], case_sensitive=False), default=None, help="Project type")
@click.pass_context
def add(ctx: Context,  path: str | None, name: str | None, type: str | None):
    while True:
        project_path = file_service.reader.select_folder()
        # project_path: str = Commander.persistent_input("Enter Project Path")
        if file_service.file_exists(project_path):
            project = self.find_by_path(project_path)
            if project is None:
                break
            else:
                click.secho(f"Invalid path. It already exists.")
                continue
        click.secho(f"Invalid path. Does not exist: {project_path}")
        project_name = file_service.extract_sub_directory_from_path(project_path)
        if type is None:
            project_type = ProjectType.get_type(project_path)
        else:
            project_type = ProjectType(type.capitalize()) if type else ProjectType.UNKNOWN
        project_id = self.db.insert(new_project)
        new_project = ProjectModel(
            path=project_path,
            name=project_name,
            type=project_type.value,
        )
        click.secho("Project created", fg="green")
        # FIXME: Update the active path later
        #  self.update_project_path_config(project_id)

