import httpx


async def get_input_data(client: httpx.AsyncClient, day: int, year: int) -> str:
    url = rf"https://adventofcode.com/{year}/day/{day}/input"
    response = await client.get(url)
    response.raise_for_status()
    return response.text
