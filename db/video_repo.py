"""
Video repository - Database CRUD operations for videos
"""
from db.database import get_connection


def insert_video(video_id: str, file_id: str, caption: str, channel_message_id: int) -> None:
    """
    Insert a video into the database
    
    Args:
        video_id: The video identifier (e.g., "25.11.2022")
        file_id: Telegram file_id of the video
        caption: Video caption text
        channel_message_id: Message ID of the forwarded video in the channel
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO videos (video_id, file_id, caption, channel_message_id) VALUES (?, ?, ?, ?)",
        (video_id, file_id, caption, channel_message_id)
    )
    
    conn.commit()
    conn.close()


def get_videos_by_id(video_id: str) -> list[dict]:
    """
    Get all videos by video ID
    
    Args:
        video_id: The video identifier to search for
    
    Returns:
        List of dictionaries containing video data (id, video_id, file_id, created_at)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT id, video_id, file_id, caption, channel_message_id, created_at
        FROM videos
        WHERE video_id = ?
        """,
        (video_id,)
    )
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convert Row objects to dictionaries
    return [dict(row) for row in rows]


def delete_by_video_id(video_id: str) -> int:
    """
    Delete all videos by video ID

    Returns:
        Number of rows deleted
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM videos WHERE video_id = ?", (video_id,))
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted
