from fastapi import APIRouter, status, Query, HTTPException
from language_tool_python import LanguageTool
from models import MarkdownText, write_file, read_file
from markdown import markdown
import os

tool = LanguageTool('en-US')
router = APIRouter(prefix='/api/markdown', tags=['markdown'])
parentdir = '/Users/methiinn/Desktop/coding/roadmapsh/Markdown-Note-taking-App/project/uploads'

@router.post('/grammar')
async def check_grammar(markdown: MarkdownText):
    matches = tool.check(markdown.markdownText)

    issues = [
        {"error": match.message, "suggestions": match.replacements, "offset": match.offset, "length": match.errorLength}
        for match in matches
    ]

    return {'issues': issues}

@router.post('/new-note', status_code=status.HTTP_201_CREATED)
async def add_note(markdown: MarkdownText):
    file_name = f'upload_{len(os.listdir(parentdir)) + 1}.md'
    path = os.path.join(parentdir, file_name)
    await write_file(path, markdown.markdownText)

@router.get('/notes', status_code=status.HTTP_200_OK)
async def get_all_notes():
    folders = os.listdir(parentdir)
    data = []
    for folder in folders:
        path = os.path.join(parentdir, folder)
        text = await read_file(path)
        data.append(text)

    return data

@router.get('/file-as-html')
async def render_file(file_name: str = Query(...)):
    file_path = os.path.join(parentdir, file_name)
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found.")
    markdown_content = await read_file(file_path)
    html_content = markdown(markdown_content)
    return {"html": html_content}