"""
Video service - Business logic for video operations
"""
from db import video_repo
from services.validation import is_valid_video_id


def save_video(video_id: str, file_id: str, caption: str, channel_message_id: int) -> None:
    """
    Save a video to the database
    
    Args:
        video_id: The video identifier
        file_id: Telegram file_id of the video
        caption: Caption text sent with the video
        channel_message_id: Message ID of the forwarded video in the channel
    
    Raises:
        ValueError: If video_id format is invalid
    """
    if not is_valid_video_id(video_id):
        raise ValueError(f"Invalid video ID format: {video_id}")
    
    video_repo.insert_video(video_id, file_id, caption or "", channel_message_id)


def get_videos(video_id: str) -> list[dict]:
    """
    Get all videos by video ID
    
    Args:
        video_id: The video identifier to search for
    
    Returns:
        List of video dictionaries (empty list if not found)
    """
    if not video_id:
        return []
    
    return video_repo.get_videos_by_id(video_id.strip())
