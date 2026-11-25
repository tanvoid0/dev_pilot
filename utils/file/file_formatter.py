import yaml


class FileFormatter:
    @staticmethod
    def format_yaml(file):
        return yaml.safe_load(file)
