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
openai.api_key = os.getenv("OPENAI_API_KEY")

# load config.toml
try:
    config = toml.load("config.toml")["chat"]
except:
    config = {model: "gpt-3.5-turbo-16k"} 

default_user = {"user": {"name": "user", "bio": "you know nothing about me", "style": "bold magenta"}}
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


# functions
def extract_code_blocks(text):
    pattern = r"```python\n(.*?)\n```"
    code_blocks = re.findall(pattern, text, re.DOTALL)
    return code_blocks


# chat
def chat_run():
    codai(end="")
    console.print(help_message)

    # Chat history
    messages = []
    messages.append({"role": "user", "content": system})

    while True:
        user_str = config["user"]["name"]
        console.print(f"(codai) {user_str}@dkdc.ai", style=config["user"]["style"], end="")
        console.print(" % ", style="bold white", end="")
        user_input = console.input()
        codai()

        if user_input.lower().strip() in ["/exit", "/quit", "/q"]:
            log.info("Exiting...")
            break

        elif user_input.lower().strip() in ["clear"]:
            console.clear()

        elif user_input.lower().startswith("/"):
            if user_input.lower().startswith("/ls"):
                os.system("ls -1phG -a")

            elif user_input.lower().startswith("/read"):
                try:
                    filename = user_input.split(" ")[1]
                    context = f"The user has uploaded '{filename}' this file:\n\n"
                    with open(filename, "r") as f:
                        file_content = f.read()
                        messages.append(
                            {"role": "system", "content": context + file_content}
                        )
                        console.print(f"Successfully read '{filename}' into context")
                except IndexError:
                    log.info("Please specify a filename.")
                except FileNotFoundError:
                    log.info("File not found.")

            elif user_input.lower().strip() == "/write":
                content = "\n".join([message["content"] for message in messages])
                # only write the last message
                filename = "temp.md"

                # Find the latest code block from the assistant's responses
                for message in messages[::-1]:
                    content = message["content"]
                    break

                with open(filename, "w") as f:
                    f.write(content)
                log.info(f"Successfully wrote conversation to '{filename}'.")

            elif user_input.lower().startswith("/write-"):
                try:
                    command = user_input.split("-")[1]

                    if command == "python":
                        filename = "temp.py"
                        code = ""

                        # Find the latest code block from the assistant's responses
                        for message in messages[::-1]:
                            code_blocks = extract_code_blocks(message["content"])
                            if message["role"] == "assistant":
                                for code_block in code_blocks:
                                    code += code_block + "\n"
                                break

                        with open(filename, "w") as f:
                            f.write(code)
                        log.info(f"Successfully wrote code to '{filename}'.")

                except IndexError:
                    log.info(
                        "Please provide a command (e.g., 'python') for the /write command."
                    )

                except Exception as e:
                    log.error(f"Error while processing the /write command: {str(e)}")

            elif user_input.lower() == "/image":
                # Generate an image summary of the conversation
                image_messages = []
                image_messages.append(
                    {
                        "role": "user",
                        "content": f"summarize this in one sentence: {messages[-1]['content']}\n",
                    }
                )

                log.info("Generating summary...")
                full_response = ""
                for response in openai.ChatCompletion.create(
                    model=config["model"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in image_messages[::-1]
                    ],
                    stream=True,
                ):
                    full_response += response.choices[0].delta.get("content", "")
                    # Flush and print out the response
                console.print(f"Summary: {full_response}")

                log.info("Generating image...")
                # Add default string placeholder
                image_str = (
                    full_response
                    + ", futuristic digital art, dark background, violet neon vibes"
                )

                response = openai.Image.create(prompt=image_str, n=1, size="512x512")
                image_url = response["data"][0]["url"]
                log.info(f"Generated image: {image_url}")

                # download image
                import requests
                from pathlib import Path
                from PIL import Image
                from io import BytesIO

                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content))
                img.save("thumbnail.png")
            else:
                log.info("Unknown command.")

        else:
            messages.append({"role": "user", "content": user_input})

            full_response = ""
            for response in openai.ChatCompletion.create(
                model=config["model"],
                messages=[
                    {"role": m["role"], "content": m["content"]} for m in messages
                ],
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                # Flush and print out the response
                console.print(response.choices[0].delta.get("content", ""), end="")

            messages.append({"role": "assistant", "content": full_response})
            print()
