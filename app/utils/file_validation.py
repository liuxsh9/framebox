"""File validation utilities."""

import re
from pathlib import Path
from typing import Optional


MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50MB in bytes


class ValidationError(Exception):
    """File validation error."""
    pass


def validate_filename(filename: str) -> str:
    """
    Validate and sanitize a filename.

    Args:
        filename: The filename to validate

    Returns:
        Sanitized filename

    Raises:
        ValidationError: If filename is invalid
    """
    if not filename:
        raise ValidationError("Filename cannot be empty")

    # Reject absolute paths
    if filename.startswith('/') or (len(filename) > 1 and filename[1] == ':'):
        raise ValidationError("Absolute paths are not allowed")

    # Reject directory traversal
    if '..' in filename:
        raise ValidationError("Directory traversal (..) is not allowed")

    # Reject non-printable characters and dangerous characters
    if not all(c.isprintable() and c not in '\x00\r\n' for c in filename):
        raise ValidationError("Filename contains invalid characters")

    # Normalize path separators
    filename = filename.replace('\\', '/')

    # Remove leading slashes
    filename = filename.lstrip('/')

    return filename


def validate_file_size(size: int, max_size: int = MAX_UPLOAD_SIZE) -> None:
    """
    Validate file size.

    Args:
        size: File size in bytes
        max_size: Maximum allowed size in bytes

    Raises:
        ValidationError: If file size exceeds limit
    """
    if size > max_size:
        raise ValidationError(f"File size {size} bytes exceeds maximum {max_size} bytes")


def validate_total_size(total_size: int, max_size: int = MAX_UPLOAD_SIZE) -> None:
    """
    Validate total upload size.

    Args:
        total_size: Total size in bytes
        max_size: Maximum allowed size in bytes

    Raises:
        ValidationError: If total size exceeds limit
    """
    if total_size > max_size:
        raise ValidationError(f"Total upload size {total_size} bytes exceeds maximum {max_size} bytes")


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing dangerous patterns.

    Args:
        filename: The filename to sanitize

    Returns:
        Sanitized filename
    """
    # Remove any null bytes
    filename = filename.replace('\x00', '')

    # Normalize to forward slashes
    filename = filename.replace('\\', '/')

    # Remove leading/trailing whitespace and slashes
    filename = filename.strip().strip('/')

    return filename
