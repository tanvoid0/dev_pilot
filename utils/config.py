import json
from pathlib import Path
from typing import Any

import click

CONFIG_DIR = Path.home() / ".config" / "cli"
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_CONFIG_DIR = Path.home() / ".config" / "cli"


class Config:
    @staticmethod
    def path():
        return "config_path"

    @staticmethod
    def _default_config():
        return {
            Config.path(): str(DEFAULT_CONFIG_DIR),
        }

    @staticmethod
    def load(config_path: Path = CONFIG_FILE):
        if not config_path.exists():
            return Config._default_config()
        with open(config_path, "r") as file:
            return json.load(file)

    @staticmethod
    def save(config: dict[str, Any]):
        if not CONFIG_DIR.exists():
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)


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
