import click
from sqlalchemy.orm import joinedload
from tabulate import tabulate

from modules.config.config import Config
from modules.config.config_model import ProjectConfigModel
from modules.project.project_model import ProjectModel, ProjectType
from utils.exception.missing_project_configuration_exception import MissingProjectConfigurationException
from utils.exception.resource_not_found_exception import ResourceNotFoundException
from utils.file.file_processor import FileProcessor
from utils.processor.commander import Commander
from utils.processor.db_processor import DBProcessor
from utils.processor.print_processor import BYELLOW_TEXT, BGREEN_TEXT, BRED_TEXT, WHITE_TEXT, color_text


class ProjectService:
    db = DBProcessor()
    config: ProjectConfigModel = None
    # config_service = ConfigService()
    # kubernetes_service = KubernetesService()
    file_service = FileProcessor()
    projects: [ProjectModel] = []
    active_project: ProjectModel | None = None

    def __init__(self, config):
        self.config = config
        self.find_active_project(safe_load=True)
        # self.refresh_project_list()

    def find_active_project(self, safe_load=False) -> ProjectModel | None:
        try:
            session = self.db.get_session()
            project = None
            if self.config.project_id is not None:
                project = (session.query(ProjectModel).filter_by(id=self.config.project_id)
                    #        .options(joinedload(ProjectModel.deployment))
                           .first())
            if project is None and not safe_load:
                raise MissingProjectConfigurationException()
            return project
        except ResourceNotFoundException as ex:
            if safe_load:
                return None
        return self.config.project_id

    def add_project(self, project_path=None, project_name=None, project_type=None):
        while project_path is None:
            if project_path is None:
                project_path = self.file_service.reader.select_folder()
            # project_path: str = Commander.persistent_input("Enter Project Path")
            if not self.file_service.file_exists(project_path):
                print(f"Invalid path. Does not exist: {project_path}")
                project_path = None
                continue
            project = self.find_by_path(project_path)
            if project is None:
                break
            else:
                print(f"Invalid path. It already exists.")
                # print(f"Invalid path. {color_text(RED_TEXT, 'It already exists.')}")
                project_path = None
                continue
        print(project_path)
        if project_name is None:
            project_name = self.file_service.extract_sub_directory_from_path(project_path)
            project_name = Commander.persistent_input("Enter Project Name", project_name)
        if project_type is None:
            project_type = ProjectType.get_type(project_path)
            print(project_type.value)
        ## FIXME: This is invalid code
        # deployment = self.kubernetes_service.get_deployments_with_cloud_data(choice=True)

        new_project = ProjectModel(
            path=project_path,
            name=project_name,
            type=project_type.value,
            # deployment_id=deployment
        )
        project_id = self.db.insert(new_project)
        self.update_project_path_config(project_id)

    def update_project_path_config(self, project_id):
        print("Updating active project:")
        project = self.find_by_id(project_id)
        config = Config.load()
        config.project.project_id = project_id
        Config.save(config.to_json())
        print(
            f"Project '{project.name}' with path {project.path} has been set to active"
            # f"Project '{color_text(BRED_TEXT, project.name)}' with path {color_text(BGREEN_TEXT, project.path)} has been set to active"
        )

    def find_by_id(self, _id: int) -> ProjectModel:
        return self.db.find_by_id(ProjectModel, _id)

    def find_by_path(self, path_name):
        session = self.db.get_session()
        project = session.query(ProjectModel).filter_by(path=path_name).first()
        return project

    def find_projects(self) -> list[ProjectModel]:
        self.projects = (self.db.get_session().query(ProjectModel)
                # .options(joinedload(ProjectModel.deployment))
                .all())
        return self.projects

    def show_projects(self):
        data = []
        header_color = BYELLOW_TEXT
        index = 1
        self.find_projects()
        self.refresh_active_project()
        for project in self.projects:
            if self.active_project is not None:
                if Commander.synthesize_path(project.path) == self.active_project.path:
                    data_color = BGREEN_TEXT
                elif not Commander.path_exist(project.path):
                    data_color = BRED_TEXT
                else:
                    data_color = WHITE_TEXT
            else:
                data_color = WHITE_TEXT
            data.append(
                (
                    color_text(data_color, index),
                    color_text(data_color, project.path),
                    color_text(data_color, project.name),
                    color_text(data_color, project.type),
                    # color_text(data_color, '' if project.deployment is None else project.deployment.name),
                    # color_text(data_color, '' if project.deployment is None else project.deployment.service_name),
                )
            )
            index += 1
        # Create a DataFrame from the list of dictionaries
        headers = [
            color_text(header_color, "Index"),
            color_text(header_color, "path"),
            color_text(header_color, "name"),
            color_text(header_color, "type"),
            # color_text(header_color, "deployment_name"),
            # color_text(header_color, "service_name"),
        ]

        # Print the DataFrame as a table
        table = tabulate(data, headers=headers, tablefmt="grid")
        click.secho(table)

    def refresh_active_project(self):
        self.active_project = self.find_active_project(safe_load=True)

    def show(self):
        print("Show projects")
        # while True:
        #     try:
        #         print(f"Total Projects: {color_text(GREEN_TEXT, str(len(self.projects)))}")
        #         self.show_projects()
        #
        #         print("s. Select Project")
        #         print("a. Add Project")
        #         # print("b. Update Project")
        #         print("r. Remove Project")
        #         print("0. Go back")
        #         choice, options = UtilProcessor.batch_picker()
        #         if choice == '0':
        #             break
        #         elif choice == 's':
        #             project = self.select_project(None if len(options) == 0 else options[0])
        #             self.update_project_path_config(project.id)
        #         elif choice == 'a':
        #             self.add_project()
        #         elif choice == 'u':
        #             project = self.select_project(None if len(options) == 0 else options[0])
        #             # self.update_project(project.id)
        #         elif choice == 'r':
        #             project = self.select_project(None if len(options) == 0 else options[0])
        #             self.remove_project(project.id)
        #         else:
        #             print("Invalid choice...")
        #             press_enter_to_continue()
        #     except AppException as ex:
        #         ex.print()
        #         press_enter_to_continue()

    def select_project(self, project_index: int = None):
        # if len(self.projects) <= 0:
        #     print("No Project to make a selection")
        #     return None
        # default_index = next((i for i, project in enumerate(self.projects) if project.id == self.active_project.id),
        #                      None)
        # if project_index is None:
        #     project_index = input(
        #         f"Enter Project Index to select ({color_text(BRED_TEXT, 0)} to exit, default :{color_text(BRED_TEXT, '0' if self.active_project is None or default_index is None else default_index)}): "
        #     )
        # if self.projects[int(project_index) - 1] == self.active_project.id:
        #     return None
        # return self.projects[int(project_index) - 1]
        pass

    def update_project(self, project_id: int, project: ProjectModel):
        raise "Implementation required"

    def remove_project(self, project_id: int):
        self.db.remove(ProjectModel, project_id)
