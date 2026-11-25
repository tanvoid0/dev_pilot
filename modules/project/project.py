from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Footer, Static, DataTable, Input
from textual.screen import ModalScreen
from textual.containers import ScrollableContainer
from textual.reactive import reactive
from textual import on
from rich.text import Text
from itertools import cycle

class ProjectAction(Static):
    def compose(self):
        yield Button("View")
        yield Button("Edit")
        yield Button("Delete")

class ProjectHeader(Static):
    def compose(self):
        yield Text("Project")

class ProjectRow(Static):
    def compose(self):
        yield Text("Project Data")


class ProjectTable(Static):
    COLUMNS = [
        'index',
        'name',
        'path',
        'type',
        'action'
    ]

    def __init__(self, data: []):
        super().__init__()
        self.data = data

    def on_mount(self):
        # self.add_columns(*self.COLUMNS)
        # for row in self.data:
        #     # Add action buttons as the last cell in each row
        #     action_cell = ProjectAction()
        #     styled_row = [
        #         Text(str(cell), justify='right') for cell in row[:-1]
        #     ]
        #     styled_row.append(action_cell)  # Add the ActionCell directly
        #     self.add_row(*styled_row)
        pass

    def on_compose(self):
        yield ProjectHeader()
        yield Text("Header")
        for row in self.data:
            yield Text("Hello")
            yield ProjectRow()

class ProjectApp(App):
    CSS_PATH = "project.css"

    ROWS = [
        ["1", "name", "path", "type"],
    ]
    COLUMNS = [
        'index',
        'name',
        'path',
        'type',
        'action'
    ]


    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        # yield Button(id="add-project", label="Add Project")
        yield DataTable()

        # with ScrollableContainer(id="table"):
        #     yield ProjectAction()
        #     yield ProjectTable(data=self.ROWS)

    def on_mount(self):
        table = self.query_one(DataTable)
        # table.cursor_type = next(cursors)
        table.zebra_stripes = True
        table.add_coumns(*self.COLUMNS)
        table.add_rows(*self.ROWS)


if __name__ == "__main__":
    ProjectApp().run()