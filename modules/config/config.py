import json
from pathlib import Path
from typing import Any

import click

from modules.config.config_model import ConfigFileModel
from utils.base_model import BaseModel
from utils.file.file_processor import FileProcessor
from utils.file.file_type import FileType
from utils.processor.db_processor import get_session, get_db_engine
from utils.processor.print_processor import color_text, GREEN_TEXT, RED_TEXT, YELLOW_TEXT

CONFIG_DIR = Path.cwd() / ".config" / "cli"
CONFIG_FILE = CONFIG_DIR / "config.json"
DB_FILE = CONFIG_DIR / "db.sqlite"
DEFAULT_CONFIG_DIR = Path.cwd() / ".config" / "cli"

file_processor = FileProcessor()


class Config:
    @staticmethod
    def first_time_setup():
        try:
            local_config = Config.load()
            Config.db_file_setup(local_config.db_reset)
            return local_config
        except Exception as ex:
            print(ex)
            raise ex

    @staticmethod
    def _default_config():
        return ConfigFileModel(path=str(DEFAULT_CONFIG_DIR))

    @staticmethod
    def load(config_path: Path = CONFIG_FILE) -> ConfigFileModel:
        if not config_path.exists():
            config = Config._default_config()
            Config.save(config.to_json())
            return config
        with open(config_path, "r") as file:
            return ConfigFileModel.from_json(json.load(file))

    @staticmethod
    def save(config: dict[str, Any]):
        if not CONFIG_DIR.exists():
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)

    @staticmethod
    def db_file_setup(reset=False):
        click.secho(f"\nDatabase Reset mode: {"On" if reset else "Off"}", fg="red" if reset else "green")
        if reset and file_processor.file_exists(DB_FILE):
            file_processor.remove(DB_FILE)
        if not file_processor.file_exists(DB_FILE):
            file_processor.write(DB_FILE, file_type=FileType.FILE)
            try:
                session = get_session()
                db_engine = get_db_engine()
                BaseModel.metadata.create_all(db_engine)
                print(color_text(YELLOW_TEXT, "Creating ") + "database")
                print("Database " + color_text(GREEN_TEXT, "created\n"))

                print(color_text(GREEN_TEXT, "Setting up") + " runtime vars")

                session.commit()
            except Exception as ex:
                print("Database Connection Failed {}".format(ex))
                raise ex
            return True
        return False


@click.group()
def config():
    """Configuration options"""
    pass


@config.command()
@click.argument("pair")
@click.pass_context
def create(ctx: click.Context, pair: str):
    """Set a configuration key-value pair."""
    try:
        key, value = pair.split("=", 1)
        click.secho(f"Key: {key}", fg="green")
        click.secho(f"Value: {value}", fg="blue")
        config = ctx.obj.get("config", {})
        config[key] = value
        ctx.obj["config"] = config
        Config.save(config)
    except ValueError:
        click.secho("Error: Please provide input in the format 'key=value'.", fg="red")


@config.command()
@click.argument("key", required=False)
@click.pass_context
def read(ctx: click.Context, key: str):
    """Read a configuration value by key or print all key-value pairs."""
    config = ctx.obj.get("config", {})

    if key is None:
        # Print all key-value pairs
        if config:
            for k, v in config.items():
                click.secho(f"{k}={v}", fg="green")
        else:
            click.secho("No config data found.", fg="red")
    else:
        # Read the value for the specified key
        value = config.get(key)
        if value is not None:
            click.secho(f"{key}={value}", fg="green")
        else:
            click.secho(f"Error: Key '{key}' not found in config.", fg="red")


@config.command()
@click.argument("key")
@click.pass_context
def remove(ctx: click.Context, key: str):
    """Remove a configuration value by key."""
    config = ctx.obj.get("config", {})
    value = config.get(key)
    if value is not None:
        click.secho(f"Removed {key} from config", fg="red")
        del config[key]
        ctx.obj["config"] = config
        Config.save(config)
    else:
        click.secho(f"Error: Key '{key}' not found in config.", fg="red")
