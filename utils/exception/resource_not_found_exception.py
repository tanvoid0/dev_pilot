from utils.exception.app_exception import AppException


class ResourceNotFoundException(AppException):
    def __init__(self, resource_name, property_name, property_value):
        self.resource_name = resource_name
        self.property_name = property_name
        self.property_value = property_value
        super().__init__(f"{resource_name} with {property_name}={property_value} not found.")
