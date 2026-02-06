"""Database layer with SQLite schema and CRUD operations."""

import aiosqlite
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
import os


class Database:
    """Async SQLite database manager."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._conn: Optional[aiosqlite.Connection] = None

    async def connect(self) -> aiosqlite.Connection:
        """Get or create database connection."""
        if self._conn is None:
            os.makedirs(Path(self.db_path).parent, exist_ok=True)
            self._conn = await aiosqlite.connect(self.db_path)
            self._conn.row_factory = aiosqlite.Row
        return self._conn

    async def close(self):
        """Close database connection."""
        if self._conn:
            await self._conn.close()
            self._conn = None

    async def init_db(self):
        """Initialize database schema with tables and indexes."""
        conn = await self.connect()

        await conn.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                entry_file TEXT DEFAULT 'index.html'
            )
        """)

        await conn.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id TEXT NOT NULL,
                filename TEXT NOT NULL,
                size INTEGER NOT NULL,
                uploaded_at TEXT NOT NULL,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
                UNIQUE(project_id, filename)
            )
        """)

        # Create indexes
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_projects_name ON projects(name)")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_files_project ON files(project_id)")

        await conn.commit()

    # Project CRUD operations

    async def create_project(self, project_id: str, name: str, entry_file: str = "index.html") -> Dict[str, Any]:
        """Create a new project."""
        conn = await self.connect()
        now = datetime.utcnow().isoformat()

        await conn.execute(
            "INSERT INTO projects (id, name, created_at, updated_at, entry_file) VALUES (?, ?, ?, ?, ?)",
            (project_id, name, now, now, entry_file)
        )
        await conn.commit()

        return {
            "id": project_id,
            "name": name,
            "created_at": now,
            "updated_at": now,
            "entry_file": entry_file
        }

    async def get_project_by_id(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get project by ID."""
        conn = await self.connect()
        cursor = await conn.execute(
            "SELECT * FROM projects WHERE id = ?",
            (project_id,)
        )
        row = await cursor.fetchone()
        return dict(row) if row else None

    async def get_project_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get project by name."""
        conn = await self.connect()
        cursor = await conn.execute(
            "SELECT * FROM projects WHERE name = ?",
            (name,)
        )
        row = await cursor.fetchone()
        return dict(row) if row else None

    async def list_projects(self, search: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """List all projects with optional search and limit."""
        conn = await self.connect()

        query = "SELECT * FROM projects"
        params = []

        if search:
            query += " WHERE name LIKE ?"
            params.append(f"%{search}%")

        query += " ORDER BY created_at DESC"

        if limit:
            query += " LIMIT ?"
            params.append(limit)

        cursor = await conn.execute(query, params)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

    async def update_project(self, project_id: str, name: Optional[str] = None,
                           entry_file: Optional[str] = None) -> bool:
        """Update project metadata."""
        conn = await self.connect()
        now = datetime.utcnow().isoformat()

        updates = []
        params = []

        if name is not None:
            updates.append("name = ?")
            params.append(name)

        if entry_file is not None:
            updates.append("entry_file = ?")
            params.append(entry_file)

        if not updates:
            return False

        updates.append("updated_at = ?")
        params.append(now)
        params.append(project_id)

        query = f"UPDATE projects SET {', '.join(updates)} WHERE id = ?"
        await conn.execute(query, params)
        await conn.commit()

        return True

    async def delete_project(self, project_id: str) -> bool:
        """Delete a project (files cascade automatically)."""
        conn = await self.connect()
        cursor = await conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        await conn.commit()
        return cursor.rowcount > 0

    # File CRUD operations

    async def add_file(self, project_id: str, filename: str, size: int) -> Dict[str, Any]:
        """Add or update file metadata."""
        conn = await self.connect()
        now = datetime.utcnow().isoformat()

        # Use INSERT OR REPLACE for incremental updates
        await conn.execute("""
            INSERT INTO files (project_id, filename, size, uploaded_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(project_id, filename)
            DO UPDATE SET size = excluded.size, uploaded_at = excluded.uploaded_at
        """, (project_id, filename, size, now))
        await conn.commit()

        return {
            "project_id": project_id,
            "filename": filename,
            "size": size,
            "uploaded_at": now
        }

    async def list_files(self, project_id: str) -> List[Dict[str, Any]]:
        """List all files for a project."""
        conn = await self.connect()
        cursor = await conn.execute(
            "SELECT filename, size, uploaded_at FROM files WHERE project_id = ? ORDER BY filename",
            (project_id,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

    async def delete_file(self, project_id: str, filename: str) -> bool:
        """Delete a file record."""
        conn = await self.connect()
        cursor = await conn.execute(
            "DELETE FROM files WHERE project_id = ? AND filename = ?",
            (project_id, filename)
        )
        await conn.commit()
        return cursor.rowcount > 0


# Global database instance
db: Optional[Database] = None


def get_db() -> Database:
    """Get the global database instance."""
    if db is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    return db


async def init_database(db_path: str):
    """Initialize the global database instance."""
    global db
    db = Database(db_path)
    await db.init_db()


async def close_database():
    """Close the global database instance."""
    global db
    if db:
        await db.close()
        db = None
