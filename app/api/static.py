"""Static file serving endpoints."""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from pathlib import Path
import mimetypes

from app.database import get_db
from app.config import settings


router = APIRouter(prefix="/view", tags=["static"])


async def resolve_project(id_or_name: str):
    """Resolve project by ID or name."""
    db = get_db()

    # Try as ID first (6 character string)
    if len(id_or_name) == 6:
        project = await db.get_project_by_id(id_or_name)
        if project:
            return project

    # Try as name
    project = await db.get_project_by_name(id_or_name)
    if project:
        return project

    return None


@router.get("/{id_or_name}/")
@router.get("/{id_or_name}")
async def serve_entry_file(id_or_name: str):
    """Serve the project's entry file."""
    project = await resolve_project(id_or_name)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{id_or_name}' not found"
        )

    # Get entry file path
    project_dir = Path(settings.projects_dir) / project['id']
    file_path = project_dir / project['entry_file']

    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entry file '{project['entry_file']}' not found"
        )

    # Determine content type
    content_type, _ = mimetypes.guess_type(str(file_path))
    if content_type is None:
        content_type = "application/octet-stream"

    return FileResponse(
        path=file_path,
        media_type=content_type,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )


@router.get("/{id_or_name}/{filepath:path}")
async def serve_file(id_or_name: str, filepath: str):
    """Serve any file from a project."""
    project = await resolve_project(id_or_name)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{id_or_name}' not found"
        )

    # Get file path
    project_dir = Path(settings.projects_dir) / project['id']
    file_path = project_dir / filepath

    # Security: ensure file is within project directory
    try:
        file_path = file_path.resolve()
        project_dir = project_dir.resolve()
        if not str(file_path).startswith(str(project_dir)):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File '{filepath}' not found"
        )

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File '{filepath}' not found"
        )

    # Determine content type
    content_type, _ = mimetypes.guess_type(str(file_path))
    if content_type is None:
        content_type = "application/octet-stream"

    return FileResponse(
        path=file_path,
        media_type=content_type,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )
