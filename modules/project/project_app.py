from itertools import cycle
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Static, Button
from textual.screen import Screen


# Sample data for projects
ROWS = [
    ("Project Name", "Path", "Type"),
    ("Project1", "/home/user/projects/project1", "Development"),
    ("ProjectX", "/home/user/projects/projectX", "Research"),
    ("App", "/home/user/projects/app", "Development"),
    ("Website", "/home/user/projects/website", "Design"),
    ("API", "/home/user/projects/api", "Development"),
]


class ProjectDetailsScreen(Screen):
    """Screen to show project details."""

    def __init__(self, project_name, project_path, project_type):
        super().__init__()
        self.project_name = project_name
        self.project_path = project_path
        self.project_type = project_type

    def compose(self) -> ComposeResult:
        """Define layout for project details screen."""
        yield Static(f"Project Name: {self.project_name}")
        yield Static(f"Path: {self.project_path}")
        yield Static(f"Type: {self.project_type}")
        yield Button("Back", id="back_button")  # Button to go back

    def on_click(self, event) -> None:
        """Handle click events (e.g., back button)."""
        if event.button.id == "back_button":
            self.dismiss()


class ProjectManagerScreen(Screen):
    """Project management CRUD application."""

    def __init__(self):
        super().__init__()
        self.selected_row = None  # Track selected row index

    def compose(self) -> ComposeResult:
        """Define layout with DataTable and Static widget for row selection display."""
        yield Static("Row Selected: None", id="row_selected")  # Display selected row
        yield DataTable(id="project_table")  # Explicitly set id for querying

    def on_mount(self) -> None:
        """Populate the table when the app is mounted."""
        table = self.query_one("#project_table", DataTable)  # Query by custom id
        table.cursor_type = 'row'  # Set initial cursor type
        table.zebra_stripes = True  # Enable zebra striping (alternating row colors)
        table.add_columns(*ROWS[0])  # Add columns from the first row of data
        table.add_rows(ROWS[1:])  # Add the remaining rows

    def on_key(self, event) -> None:
        """Handle key events for row selection and navigation."""
        table = self.query_one("#project_table", DataTable)  # Query by custom id
        if event.key == "enter":
            self.update_selected_row(table)  # Update the "Row Selected" display
            self.show_project_details(table)  # Show project details screen

    def update_selected_row(self, table: DataTable):
        """Update the display of selected row info."""
        row_selected_display = self.query_one("#row_selected", Static)
        row_index = table.cursor_coordinate.row  # Get the row index of the selected cursor
        if row_index is not None:
            row_data = table.get_row_at(row_index)  # Get the row data at selected index
            row_selected_display.update(f"Row Selected: {row_data[0]}")  # Display project name
        else:
            row_selected_display.update("Row Selected: None")

    def show_project_details(self, table: DataTable):
        """Switch to the project details screen."""
        row_index = table.cursor_coordinate.row  # Get the row index of the selected cursor
        if row_index is not None:
            row_data = table.get_row_at(row_index)  # Get the row data at selected index
            project_name = row_data[0]
            project_path = row_data[1]
            project_type = row_data[2]

            # Push the project details screen with the project info
            self.app.push_screen(ProjectDetailsScreen(project_name, project_path, project_type))


class MainApp(App[None]):
    """Main application that uses ProjectManagerScreen for project management."""

    def compose(self) -> ComposeResult:
        """Add the ProjectManagerScreen to the app."""
        yield ProjectManagerScreen()  # Add the ProjectManagerScreen as the initial screen

    def on_mount(self) -> None:
        """Ensure the screen gets rendered immediately."""
        self.push_screen(ProjectManagerScreen())  # Push the main screen when the app starts


# Run the app
app = MainApp()
if __name__ == "__main__":
    app.run()
