from time import monotonic

import click
from textual.app import App
from textual.widgets import Button, Header, Footer, Static
from textual.containers import ScrollableContainer
from textual.reactive import reactive
from textual import on


class TimeDisplay(Static):
    """Custom time display widget."""

    accumulated_time = 0
    start_time = monotonic()
    time_elapsed = reactive(0)

    def on_mount(self):
        self.update_timer = self.set_interval(
            1 / 60,
            self.update_time_elapsed,
            pause=True
        )

    def update_time_elapsed(self):
        self.time_elapsed = self.accumulated_time + (monotonic() - self.start_time)

    def watch_time_elapsed(self):
        time = self.time_elapsed
        time, seconds = divmod(time, 60)
        hours, minutes = divmod(time, 60)
        time_string = f"{hours:02.0f}:{minutes:02.0f}:{seconds:05.2f}"
        self.update(time_string)

    def start(self):
        """Start keeping track of the time elapsed."""
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self):
        """Stop keeping track of the time elapsed."""
        self.accumulated_time = self.time_elapsed
        self.update_timer.pause()

    def reset(self):
        """Reset keeping track of the time elapsed."""
        self.accumulated_time = 0
        self.time_elapsed = 0
        self.update_timer.pause()


class Stopwatch(Static):
    """Custom stopwatch widget."""

    @on(Button.Pressed, '#start')
    def start_stopwatch(self):
        self.add_class("started")
        self.query_one(TimeDisplay).start()

    @on(Button.Pressed, '#stop')
    def stop_stopwatch(self):
        self.remove_class("started")
        self.query_one(TimeDisplay).stop()

    @on(Button.Pressed, '#reset')
    def reset_stopwatch(self):
        self.remove_class("started")
        self.query_one(TimeDisplay).reset()

    def compose(self):
        yield Button("Start", variant="success", id="start")
        yield Button("Stop", variant="error", id="stop")
        yield Button("Reset", id="reset")
        yield TimeDisplay("00:00:00.00")


class StopwatchApp(App):
    BINDINGS = [
        ('d', 'toggle_dark_mode', 'Toggle dark mode'),
        ('a', 'add_stopwatch', 'Add'),
        ('r', 'remove_stopwatch', 'Remove'),
    ]

    CSS_PATH = 'stopwatch.tcss'

    # Alternative
    # CSS = """
    # Stopwatch {
    #     layout: horizontal;
    # }
    # """

    def compose(self):
        """What widgets is this app composed of?"""
        yield Header(show_clock=True)
        yield Footer()
        # yield Button("Stop all")
        with ScrollableContainer(id="stopwatches"):
            yield Stopwatch()
            yield Stopwatch()
            yield Stopwatch()

        """ Alternative
        yield ScrollableContainer(
            Stopwatch(),
            Stopwatch(),
            Stopwatch(),
            id="stopwatches",
        )
        """

    def action_toggle_dark_mode(self):
        self.theme = 'solarized-light' if self.theme == 'nord' else 'nord'

    def action_add_stopwatch(self):
        stopwatch = Stopwatch()
        container = self.query_one("#stopwatches")
        container.mount(stopwatch)
        stopwatch.scroll_visible()

    def action_remove_stopwatch(self):
        stopwatches = self.query(Stopwatch)
        if stopwatches:
            stopwatches.last().remove()


@click.command
def stopwatch():
    StopwatchApp().run()


if __name__ == "__main__":
    stopwatch()
