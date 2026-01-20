"""
Validation module - ID format validation using regex
"""
import re


# Regex pattern for valid video IDs:
# - 25.11.2022 (required format)
# - 25.11.2022.1 (optional suffix)
# - 25.11.2022.2 (optional suffix)
VIDEO_ID_PATTERN = re.compile(r'^\d{1,2}\.\d{1,2}\.\d{4}(\.\d+)?$')


def is_valid_video_id(video_id: str) -> bool:
    """
    Validate video ID format
    
    Valid formats:
    - 25.11.2022
    - 25.11.2022.1
    - 25.11.2022.2
    
    Args:
        video_id: The video ID string to validate
    
    Returns:
        True if valid, False otherwise
    """
    if not video_id or not isinstance(video_id, str):
        return False
    
    return bool(VIDEO_ID_PATTERN.match(video_id.strip()))
