"""Project management API endpoints."""

from fastapi import APIRouter, HTTPException, status
from typing import Optional
import shutil
from pathlib import Path

from app.models import ProjectCreate, ProjectResponse, ProjectUpdate, ListProjectsResponse
from app.database import get_db
from app.utils.id_generator import generate_unique_id
from app.config import settings


router = APIRouter(prefix="/api/projects", tags=["projects"])


async def check_project_exists(project_id: str) -> bool:
    """Check if a project with given ID exists."""
    db = get_db()
    project = await db.get_project_by_id(project_id)
    return project is not None


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate):
    """Create a new project."""
    db = get_db()

    # Check if name already exists
    existing = await db.get_project_by_name(project.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Project with name '{project.name}' already exists"
        )

    # Generate unique ID
    project_id = await generate_unique_id(check_project_exists)

    # Create project in database
    created = await db.create_project(project_id, project.name, project.entry_file)

    # Create project directory
    project_dir = Path(settings.projects_dir) / project_id
    project_dir.mkdir(parents=True, exist_ok=True)

    return ProjectResponse(**created)


@router.get("", response_model=ListProjectsResponse)
async def list_projects(search: Optional[str] = None, limit: Optional[int] = None):
    """List all projects with optional search and limit."""
    db = get_db()
    projects = await db.list_projects(search=search, limit=limit)

    return ListProjectsResponse(
        projects=[ProjectResponse(**p) for p in projects],
        total=len(projects)
    )


@router.get("/{id_or_name}", response_model=ProjectResponse)
async def get_project(id_or_name: str):
    """Get a project by ID or name."""
    db = get_db()

    # Try as ID first (6 character string)
    if len(id_or_name) == 6:
        project = await db.get_project_by_id(id_or_name)
        if project:
            return ProjectResponse(**project)

    # Try as name
    project = await db.get_project_by_name(id_or_name)
    if project:
        return ProjectResponse(**project)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Project '{id_or_name}' not found"
    )


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: str, update: ProjectUpdate):
    """Update project metadata."""
    db = get_db()

    # Check if project exists
    existing = await db.get_project_by_id(project_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{project_id}' not found"
        )

    # If updating name, check for conflicts
    if update.name:
        name_conflict = await db.get_project_by_name(update.name)
        if name_conflict and name_conflict['id'] != project_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Project with name '{update.name}' already exists"
            )

    # Update project
    await db.update_project(
        project_id,
        name=update.name,
        entry_file=update.entry_file
    )

    # Get updated project
    updated = await db.get_project_by_id(project_id)
    return ProjectResponse(**updated)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: str):
    """Delete a project and all its files."""
    db = get_db()

    # Check if project exists
    existing = await db.get_project_by_id(project_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{project_id}' not found"
        )

    # Delete from database (files cascade automatically)
    await db.delete_project(project_id)

    # Delete project directory
    project_dir = Path(settings.projects_dir) / project_id
    if project_dir.exists():
        shutil.rmtree(project_dir)
