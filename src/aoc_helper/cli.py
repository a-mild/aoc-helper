import asyncio
from datetime import date
import os
from pathlib import Path
from typing import Annotated, Optional
import httpx
import typer

from aoc_helper import get_input_data

app = typer.Typer()


def current_year() -> int:
    return date.today().year


def current_day() -> int:
    return date.today().day


@app.command()
def setup(
    day: Annotated[int, typer.Argument(default_factory=current_day)],
    year: Annotated[int, typer.Argument(default_factory=current_year)],
    session_cookie: Annotated[Optional[str], typer.Option()] = None,
) -> None:
    if session_cookie is None:
        session_cookie = os.getenv("AOC_SESSION_COOKIE")
    if session_cookie is None:
        session_cookie = typer.prompt("Enter your session cookie", type=str)

    filepath = Path.cwd() / f"{year}" / f"{day:0>2}" / "input.txt"
    if not filepath.exists():
        filepath.parent.mkdir(parents=True, exist_ok=True)

    async def dummy() -> str:
        async with httpx.AsyncClient(cookies={"session": session_cookie}) as client:
            try:
                input_data = await get_input_data(client, day, year)
            except httpx.RequestError as e:
                typer.Abort(e)
            return input_data

    input_data = asyncio.run(dummy())
    with open(filepath, "w") as f:
        f.write(input_data)


if __name__ == "__main__":
    app()
