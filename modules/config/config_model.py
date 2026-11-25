class ProjectConfigModel:
    project_id: str

    def __init__(self, project_id=None):
        self.project_id = project_id

class _DockerConfigModel:
    pre_tag: str
    post_tag: str

    def __init__(self, pre_tag=None, post_tag=None):
        self.pre_tag = pre_tag
        self.post_tag = post_tag

class ConfigFileModel:
    path: str
    db_reset: bool
    project: ProjectConfigModel
    docker: _DockerConfigModel

    def __init__(self,
                 path: str = None,
                 db_reset: bool=False,
                 project: ProjectConfigModel=ProjectConfigModel(),
                 docker: _DockerConfigModel = _DockerConfigModel(),
                 ):
        self.path = path
        self.db_reset = db_reset
        self.project = project
        self.docker = docker

    def to_json(self):
        return {
            'path': self.path,
            'db_reset': self.db_reset,
            'project': {
                'project_id': self.project.project_id,
            },
            'docker': {
                'pre_tag': self.docker.pre_tag,
                'post_tag': self.docker.post_tag,
            }
        }

    @staticmethod
    def from_json(json):
        return ConfigFileModel(
            path=json['path'],
            db_reset=json['db_reset'],
            project=ProjectConfigModel(json['project']['project_id']),
            docker=_DockerConfigModel(json['docker']['pre_tag'], json['docker']['post_tag']),
        )