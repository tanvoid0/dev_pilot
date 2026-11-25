from __future__ import annotations

from modules.dictionary.translator import Translator

try:
    import httpx
except ImportError:
    raise ImportError("Please install httpx with 'pip install httpx' ")

try:
    from wiktionaryparser import WiktionaryParser
except ImportError:
    raise ImportError("Please install wiktionaryparser with 'pip install wiktionaryparser' ")


from textual import work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll, Horizontal, Grid
from textual.widgets import Input, Markdown, Select


class DictionaryApp(App):
    """Searches a dictionary API as-you-type."""

    CSS_PATH = "dictionary.tcss"
    languages = ['english', 'french', 'bangla']
    default_language = 'english'
    parser = WiktionaryParser()

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search for a word", id="dictionary-search")
        # yield Select([(lang.capitalize(), lang) for lang in self.languages], value="english")
        with VerticalScroll(id="results-container"):
            yield Markdown(id="results")

    async def on_input_changed(self, message: Input.Changed) -> None:
        """A coroutine to handle a text changed message."""
        if message.value:
            self.lookup_word(message.value)
        else:
            # Clear the results
            await self.query_one("#results", Markdown).update("")

    @work(exclusive=True)
    async def lookup_word(self, word: str) -> None:
        try:
            if not word or len(word) == 0:
                return
            results = await Translator.translate(word)
            if word == self.query_one(Input).value:
                markdown = self.make_word_markdown(results)
                await self.query_one("#results", Markdown).update(markdown)
        except Exception:
            await self.query_one("#results", Markdown).update(results)

    def make_word_markdown(self, results: object) -> str:
        """Convert the results into markdown."""
        lines = []
        if isinstance(results, dict):
            lines.append(f"# {results['title']}")
            lines.append(results["message"])
        elif isinstance(results, list):
            for result in results:
                lines.append(f"# {result['word']}")
                lines.append("")
                for meaning in result.get("meanings", []):
                    lines.append(f"_{meaning['partOfSpeech']}_")
                    lines.append("")
                    for definition in meaning.get("definitions", []):
                        lines.append(f" - {definition['definition']}")
                    lines.append("---")

        return "\n".join(lines)


if __name__ == "__main__":
    app = DictionaryApp()
    app.run()