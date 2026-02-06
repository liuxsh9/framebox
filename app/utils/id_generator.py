"""ID generation utilities for projects."""

from nanoid import generate


def generate_id(size: int = 6) -> str:
    """
    Generate a short, URL-safe ID using nanoid.

    Args:
        size: Length of the ID (default 6 characters)

    Returns:
        A random URL-safe string
    """
    return generate(size=size)


async def generate_unique_id(check_exists_fn, size: int = 6, max_attempts: int = 10) -> str:
    """
    Generate a unique ID with collision detection.

    Args:
        check_exists_fn: Async function that checks if ID exists (returns bool)
        size: Length of the ID
        max_attempts: Maximum number of generation attempts

    Returns:
        A unique ID

    Raises:
        RuntimeError: If unable to generate unique ID after max_attempts
    """
    for _ in range(max_attempts):
        project_id = generate_id(size)
        if not await check_exists_fn(project_id):
            return project_id

    raise RuntimeError(f"Failed to generate unique ID after {max_attempts} attempts")
