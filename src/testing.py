# imports
import re
import os
import toml
import typer
import openai

import logging as log

from rich import print
from rich.console import Console
from dotenv import load_dotenv

# load .env file
load_dotenv()

# openai config
openai.api_type = "azure"
openai.api_base = "https://birdbrain.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

model = "birdbrain-4-32k"

# load config.toml
try:
    config = toml.load("config.toml")["icode"]
except:
    config = {"model": "gpt-3.5-turbo-16k"}

default_user = {
    "user": {
        "name": "user",
        "bio": "you know nothing about me",
        "style": "bold magenta",
    }
}
if "user" not in config:
    config.update(default_user)

for key in default_user["user"]:
    if key not in config["user"]:
        config["user"][key] = default_user["user"][key]

# configure logger
log.basicConfig(level=log.INFO)

# configure rich
console = Console()

# Prompt engineering
system = f"""
Hello, I am user: {config["user"]}
"""

# read in system message from 'system.md'
with open("system.md", "r") as f:
    system_message = f.read()

system += f"\n{system_message}"


with open("help.md", "r") as f:
    help_message = f.read()


system += f"Help message: \n\n{help_message}"


def codai(end="\n"):
    console.print("codai", style="blink bold violet", end="")
    console.print(": ", style="bold white", end=end)


# icode
def testing_run():
    codai(end="")
    console.print(help_message)

    user_str = config["user"]["name"]
    console.print(f"(codai) {user_str}@dkdc.ai", style=config["user"]["style"], end="")
    console.print(" % ", style="bold white", end="")
    user_input = console.input()
    codai()
    console.print(user_input, style="bold white")

    messages = []
    messages.append({"role": "user", "content": user_input})

    log.info("Responding...")
    full_response = ""
    for response in openai.ChatCompletion.create(
        engine=model,
        messages=messages,
        stream=True,
        temperature=0.7,
        max_tokens=1600,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    ):
        full_response += response.choices[0].delta.get("content", "")
        # Flush and print out the response
    console.print(f"{full_response}")
