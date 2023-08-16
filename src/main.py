# imports
import os
import sys
import toml
import typer

from dotenv import load_dotenv

## local imports
from .icode import icode_run
from .testing import testing_run

# configuration
## load .env file
load_dotenv()

## load config
try:
    config = toml.load("config.toml")
except FileNotFoundError:
    config = {}

## typer config
app = typer.Typer(no_args_is_help=True)


## global options
def version(value: bool):
    if value:
        version = toml.load("pyproject.toml")["project"]["version"]
        typer.echo(f"{version}")
        raise typer.Exit()


# subcommands
@app.command()
def icode():
    """
    interactive code
    """
    icode_run()


@app.command()
def test():
    """
    test
    """
    testing_run()


## main
@app.callback()
def main(
    version: bool = typer.Option(
        None, "--version", help="Show version.", callback=version, is_eager=True
    ),
):
    return


## if __name__ == "__main__":
if __name__ == "__main__":
    app()
