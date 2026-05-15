from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.db.repositories import repo

router = APIRouter(prefix='/api/artifacts')


class ArtifactCreate(BaseModel):
    project_id: str
    name: str
    content: str


class ArtifactUpdate(BaseModel):
    content: str


@router.post('')
async def create_artifact(payload: ArtifactCreate):
    return repo.create_artifact(payload.project_id, payload.name, payload.content)


@router.get('')
async def list_artifacts(project_id: str = Query(...)):
    return repo.list_artifacts(project_id)


@router.get('/{artifact_id}')
async def get_artifact(artifact_id: str):
    data = repo.get_artifact(artifact_id)
    if not data:
        raise HTTPException(status_code=404, detail='Artifact not found')
    return data


@router.put('/{artifact_id}')
async def update_artifact(artifact_id: str, payload: ArtifactUpdate):
    data = repo.update_artifact(artifact_id, payload.content)
    if not data:
        raise HTTPException(status_code=404, detail='Artifact not found')
    return data
