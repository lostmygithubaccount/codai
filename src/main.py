# imports
import os
import sys
import toml
import typer

from dotenv import load_dotenv
from typing_extensions import Annotated

## local imports
from .icode2 import icode_run
from .testing import testing_run
from .translate import translate_run
from .old_icode import icode_run as icode_run_old

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
def translate(
    text: Annotated[
        str, typer.Argument(help="Text to translate.")
    ] = "hello, try passing in a string to translate",
    to: Annotated[str, typer.Option(help="Language to translate to.")] = None,
    from_: Annotated[str, typer.Option("--from", help="Language to translate from.")] = None,
):
    """
    Translate from one language to another.
    """
    if "translate" in config:
        if to is None:
            if "translate" in config and "to" in config["translate"]:
                to = config["translate"]["to"]
        if from_ is None:
            if "translate" in config and "from" in config["translate"]:
                from_ = config["translate"]["from"]

    translate_run(text=text, to=to, from_=from_)


@app.command()
def icode_old():
    """
    interactive code (deprecated)
    """
    icode_run_old()


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
