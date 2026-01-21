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


async def delete_videos(bot, channel_id: int | str, video_id: str) -> dict:
    """
    Delete videos by ID: remove messages from channel and delete DB rows.

    Args:
        bot: aiogram Bot instance
        channel_id: channel id where videos are stored
        video_id: code to delete

    Returns:
        dict with counts: {"deleted_db": int, "deleted_channel": int, "failed_channel": int}
    """
    if not is_valid_video_id(video_id):
        raise ValueError(f"Invalid video ID format: {video_id}")

    videos = video_repo.get_videos_by_id(video_id.strip())
    deleted_channel = 0
    failed_channel = 0

    for video in videos:
        msg_id = video.get("channel_message_id") or 0
        if not msg_id:
            continue
        try:
            await bot.delete_message(chat_id=channel_id, message_id=msg_id)
            deleted_channel += 1
        except Exception:
            failed_channel += 1

    deleted_db = video_repo.delete_by_video_id(video_id.strip())
    return {
        "deleted_db": deleted_db,
        "deleted_channel": deleted_channel,
        "failed_channel": failed_channel,
    }
