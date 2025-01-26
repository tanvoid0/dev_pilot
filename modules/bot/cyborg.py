"""
A simple example of chatting to an LLM with Textual.

Lots of room for improvement here.

See https://textual.textualize.io/blog/2024/09/15/anatomy-of-a-textual-user-interface/

"""
import os.path
import threading
from pathlib import Path

import click
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "llm",
#     "textual",
# ]
# ///
from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Footer, Header, Input, Markdown

from utils.file_util import FileUtil

try:
    from ollama import chat
except ImportError:
    raise ImportError(
        'install the ollama package or run with "python -m pip install ollama"'
    ) from None
# The system prompt
SYSTEM = """Formulate all responses as if you where the sentient AI named Cyborg from the Alien movies."""


class Prompt(Markdown):
    """Markdown for the user prompt."""
    BORDER_TITLE = "Me"


class Response(Markdown):
    """Markdown for the reply from the LLM."""

    BORDER_TITLE = "Cyborg"


def stream_string(long_text):
    """
    Simulates streaming a long string by yielding chunks of it.

    Args:
        long_text: The long string to be streamed.

    Yields:
        Chunks of the long_text.
    """
    chunk_size = 50  # Adjust chunk size as needed
    for i in range(0, len(long_text), chunk_size):
        yield long_text[i:i + chunk_size]


class CyborgApp(App):
    """Simple app to demonstrate chatting to an LLM."""

    BINDINGS = [
        ("ctrl+c", "stop_prompt", "Stop Query"),  # Define Ctrl+C binding
        ('space', 'focus_input', 'Focus Input'),
    ]
    AUTO_FOCUS = "Input"

    CSS = """
    Prompt {
        border: wide $primary;
        background: $primary 10%;
        color: $text;
        margin: 1;        
        margin-left: 8;
        padding: 1 2 0 2;
    }

    Response {
        border: wide $success;
        background: $success 10%;   
        color: $text;             
        margin: 1;      
        margin-right: 8; 
        padding: 1 2 0 2;
    }

     .error-response {
        background: red !important;  /* Red background for stop event */
        color: white !important;      /* White text when stopped */
    }
    """
    stop_query = False
    chat_history_file = os.path.join("assets", "chat.json")

    def __init__(self):
        super().__init__()
        self.stop_event = threading.Event()
        FileUtil.create_if_not_exists(self.chat_history_file)
        cached_history = FileUtil.read_json_file(self.chat_history_file)
        self.history = [] if (cached_history is None or 'chat' not in cached_history) else cached_history['chat']

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id="chat-view"):
            yield Response("INTERFACE 2037 READY FOR INQUIRY")
        yield Input(placeholder="How can I help you?")
        yield Footer()

    async def on_mount(self) -> None:
        chat_view = self.query_one("#chat-view")
        for message in self.history:
            if message['role'] == 'user':
                await chat_view.mount(Prompt(message['content']))
            else:
                await chat_view.mount(Response(message['content']))
        chat_view.scroll_end()  # This ensures the view scrolls to the bottom


    @on(Input.Submitted)
    async def on_input(self, event: Input.Submitted) -> None:
        """When the user hits return."""
        chat_view = self.query_one("#chat-view")
        event.input.clear()
        await chat_view.mount(Prompt(event.value))
        await chat_view.mount(response := Response())
        response.anchor()

        self.query_one(Input).blur()
        self.stop_event.clear()
        self.send_prompt(event.value, response)

    @work(thread=True)
    def send_prompt(self, prompt: str, response: Response) -> None:
        """Get the response in a thread."""

        self.history.append({
            'role': 'user',
            'content': prompt,
        })

        response_content = ""
        try:
            llm_response = chat(model='llama3.2', messages=self.history, stream=True)
            for chunk in llm_response:
                if self.stop_event.is_set():  # Check the stop event
                    response_content += "\n\n[b]!!Prompt Stopped!!![/b]"
                    # Dynamically change the background color to red
                    self.call_from_thread(response.update, response_content)
                    self.call_from_thread(response.add_class, "error-response")
                    break
                if 'content' in chunk['message']:
                    response_content += chunk['message']['content']
                    self.call_from_thread(response.update, response_content)
            if response_content:
                self.history.append({
                    'role': 'assistant',
                    'content': response_content,
                })
        except Exception as e:
            self.notify(f"Oops! Something went wrong: {e}", severity="error", timeout=10)
        finally:
            self.action_focus_input()
            chat_history = FileUtil.read_json_file(self.chat_history_file)
            chat_history['chat'] = self.history
            FileUtil.write_json_file(self.chat_history_file, chat_history)

    def action_stop_prompt(self):
        """Handles Ctrl+C to stop the prompt"""
        self.stop_event.set()  # Set the stop event
        self.notify("Ctrl+C Pressed. Stopping the prompt", severity="error", timeout=3)

    def action_focus_input(self):
        self.query_one(Input).focus()

@click.group()
def cyborg():
    """A cli friendly cyborg tool"""
    pass

@cyborg.command()
@click.pass_context
def run(ctx: click.Context):
    click.secho("Running CLI Cyborg", fg="green")
    CyborgApp().run()


if __name__ == "__main__":
    app = CyborgApp()
    app.run()
