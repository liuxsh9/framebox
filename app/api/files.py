"""File upload API endpoints."""

from fastapi import APIRouter, HTTPException, UploadFile, File, status
from typing import List
from pathlib import Path

from app.models import FileUploadResponse, FileInfo
from app.database import get_db
from app.utils.file_validation import validate_filename, validate_total_size, ValidationError
from app.config import settings


router = APIRouter(prefix="/api/projects", tags=["files"])


@router.post("/{project_id}/files", response_model=FileUploadResponse)
async def upload_files(project_id: str, files: List[UploadFile] = File(...)):
    """Upload multiple files to a project (incremental update)."""
    db = get_db()

    # Check if project exists
    project = await db.get_project_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{project_id}' not found"
        )

    project_dir = Path(settings.projects_dir) / project_id
    project_dir.mkdir(parents=True, exist_ok=True)

    uploaded_files = []
    total_size = 0

    try:
        # Read and validate all files first
        file_data = []
        for upload_file in files:
            content = await upload_file.read()
            file_data.append((upload_file.filename, content))
            total_size += len(content)

        # Validate total size
        validate_total_size(total_size)

        # Process each file
        for filename, content in file_data:
            # Validate and sanitize filename
            try:
                safe_filename = validate_filename(filename)
            except ValidationError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(e)
                )

            # Create directory structure for nested paths
            file_path = project_dir / safe_filename
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            file_path.write_bytes(content)

            # Update database
            await db.add_file(project_id, safe_filename, len(content))

            uploaded_files.append(safe_filename)

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )

    return FileUploadResponse(
        uploaded=uploaded_files,
        total_size=total_size
    )


@router.get("/{project_id}/files", response_model=List[FileInfo])
async def list_files(project_id: str):
    """List all files in a project."""
    db = get_db()

    # Check if project exists
    project = await db.get_project_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{project_id}' not found"
        )

    files = await db.list_files(project_id)
    return [FileInfo(**f) for f in files]
