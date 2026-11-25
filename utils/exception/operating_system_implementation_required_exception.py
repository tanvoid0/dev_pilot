import platform

from utils.exception.app_exception import AppException


class OperatingSystemImplementationRequiredAppException(AppException):
    def __init__(self, os):
        self.os = os
        if os is None:
            self.os = platform.system()

        super().__init__(f"Implementation required for OS: {self.os}")
