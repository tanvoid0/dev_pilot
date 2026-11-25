from utils.exception.app_exception import AppException


class MissingProjectConfigurationException(AppException):
    def __init__(self):
        super().__init__("One project needs to be set up first")
