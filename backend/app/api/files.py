from pathlib import Path

from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from app.db.repositories import repo

router = APIRouter(prefix='/api/files')

TEXT_EXTS = {'.txt', '.md', '.json', '.csv', '.py', '.js', '.ts', '.html', '.css'}
MAX_UPLOAD_BYTES = 2 * 1024 * 1024


def extract_text(filename: str, content: bytes) -> str:
    lower = filename.lower()
    for ext in TEXT_EXTS:
        if lower.endswith(ext):
            return content.decode('utf-8', errors='ignore')
    raise HTTPException(status_code=400, detail='Unsupported file type')


def chunk_text(text: str, size: int = 700, overlap: int = 100):
    chunks = []
    idx = 0
    start = 0
    while start < len(text):
        end = min(len(text), start + size)
        chunks.append({'id': idx, 'text': text[start:end]})
        idx += 1
        start = max(end - overlap, end)
    return chunks


@router.post('/upload')
async def upload(project_id: str = Query(...), file: UploadFile = File(...)):
    safe_name = Path(file.filename or '').name
    if safe_name != (file.filename or ''):
        raise HTTPException(status_code=400, detail='Invalid filename')
    if safe_name.startswith('.'):
        raise HTTPException(status_code=400, detail='Hidden files are blocked')
    raw = await file.read()
    if len(raw) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=400, detail='File too large')
    text = extract_text(safe_name, raw)
    chunks = chunk_text(text)
    try:
        return repo.save_file(project_id=project_id, filename=safe_name, content=raw, extracted_text=text, chunks=chunks)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get('/search')
async def search(project_id: str = Query(...), q: str = Query(...), limit: int = 5):
    return repo.search_chunks(project_id, q, limit)


@router.get('/list')
async def list_files(project_id: str = Query(...)):
    return repo.list_files(project_id)
