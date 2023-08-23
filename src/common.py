from rich.console import Console

console = Console()

def codai(end="\n"):
    console.print("codai", style="blink bold violet", end="")
    console.print(": ", style="bold white", end=end)
