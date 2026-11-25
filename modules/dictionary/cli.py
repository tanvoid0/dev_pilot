import click

from modules.dictionary.dictionary_app import DictionaryApp


@click.command
def dictionary():
    DictionaryApp().run()


if __name__ == '__main__':
    dictionary()