from pydantic import BaseModel
import aiofiles

class MarkdownText(BaseModel):
    markdownText: str

async def write_file(path: str, text: str) -> None:
    async with aiofiles.open(path, 'w') as file:
        await file.write(text)

async def read_file(path: str) -> str:
    async with aiofiles.open(path, 'r') as file:
        text = await file.read()
    return text
