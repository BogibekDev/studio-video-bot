"""
Database module - SQLite connection and initialization
"""
import sqlite3
import os
from pathlib import Path


def get_db_path() -> str:
    """Get database file path"""
    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    db_path = data_dir / "videos.db"
    return str(db_path)


def get_connection() -> sqlite3.Connection:
    """Get SQLite database connection"""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn


def init_database():
    """Initialize database tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create videos table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT NOT NULL,
            file_id TEXT NOT NULL,
            caption TEXT DEFAULT '',
            channel_message_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Backfill missing columns for existing databases
    cursor.execute("PRAGMA table_info(videos)")
    columns = {row["name"] for row in cursor.fetchall()}
    if "caption" not in columns:
        cursor.execute("ALTER TABLE videos ADD COLUMN caption TEXT DEFAULT ''")
    if "channel_message_id" not in columns:
        cursor.execute("ALTER TABLE videos ADD COLUMN channel_message_id INTEGER NOT NULL DEFAULT 0")
    
    # Create index on video_id for faster lookups
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_video_id ON videos(video_id)
    """)
    
    conn.commit()
    conn.close()
