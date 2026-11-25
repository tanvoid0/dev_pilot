import os

from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from utils.base_model import BaseModel
from enum import Enum

from utils.exception.app_exception import AppException
from utils.file.file_processor import FileProcessor


class ProjectType(Enum):
    MAVEN = "Maven"
    NPM = "Npm"
    FLUTTER = "Flutter"
    UNKNOWN = "Unknown"

    @staticmethod
    def get_type(project_path):
        file_exists = FileProcessor.file_exists

        if file_exists(os.path.join(project_path, "pom.xml")):
            return ProjectType.MAVEN
        elif file_exists(os.path.join(project_path, "package.json")):
            return ProjectType.NPM
        elif file_exists(os.path.join(project_path, "pubspec.yaml")):
            return ProjectType.FLUTTER
        else:
            return ProjectType.UNKNOWN

    @staticmethod
    def exec_func(project_type, maven=None, npm=None, flutter=None, unknown=None):
        if project_type == ProjectType.MAVEN.value:
            if maven is None:
                raise AppException("Maven Function Required")
            maven()
        elif project_type == ProjectType.NPM.value:
            if npm is None:
                raise AppException("npm Function Required")
            npm()
        elif project_type == ProjectType.FLUTTER.value:
            if flutter is None:
                raise AppException("flutter Function Required")
            flutter()
        elif project_type == ProjectType.UNKNOWN.value:
            if unknown is None:
                raise AppException("unknown Function Required")
            unknown()


class ProjectModel(BaseModel):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(String(500), unique=True)
    name: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255), default=ProjectType.UNKNOWN.value)
    # deployment_id: Mapped[int] = Column(Integer, ForeignKey('deployments.id'), nullable=True)
    # deployment: Mapped[KubernetesDeploymentModel] = relationship('KubernetesDeploymentModel', back_populates='project')
