from datetime import datetime

class AppException(Exception):
    def __init__(self, message: str):
        self.message = message
        self.timestamp = datetime.now()
        self.name = self.__class__.__name__
        super().__init__(self.message)

    def print(self):
        print(self.message)
        # print(f"{color_text(BYELLOW_TEXT, self.timestamp)}[{color_text(BRED_TEXT, self.name)}]: {self.message}")
