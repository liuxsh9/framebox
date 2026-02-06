"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field
from typing import Optional, List


class ProjectCreate(BaseModel):
    """Request model for creating a project."""
    name: str = Field(..., min_length=1, max_length=100, description="Project name")
    entry_file: str = Field(default="index.html", description="Entry file name")


class ProjectUpdate(BaseModel):
    """Request model for updating a project."""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="New project name")
    entry_file: Optional[str] = Field(None, description="New entry file name")


class ProjectResponse(BaseModel):
    """Response model for project data."""
    id: str
    name: str
    created_at: str
    updated_at: str
    entry_file: str


class FileInfo(BaseModel):
    """Model for file metadata."""
    filename: str
    size: int
    uploaded_at: str


class FileUploadResponse(BaseModel):
    """Response model for file upload."""
    uploaded: List[str]
    total_size: int


class ListProjectsResponse(BaseModel):
    """Response model for project list."""
    projects: List[ProjectResponse]
    total: int


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    uptime: float


class ServerInfoResponse(BaseModel):
    """Response model for server information."""
    host: str
    port: int
    local_ip: Optional[str] = None
    suggested_url: Optional[str] = None
