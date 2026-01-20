"""
Configuration module - reads environment variables from .env file
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_bot_token() -> str:
    """Get bot token from environment variables"""
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN not found in .env file")
    return token


def get_admin_ids() -> list[int]:
    """Get admin IDs from environment variables (comma-separated)"""
    admin_ids_str = os.getenv("ADMIN_IDS", "")
    if not admin_ids_str:
        raise ValueError("ADMIN_IDS not found in .env file")
    
    try:
        admin_ids = [int(admin_id.strip()) for admin_id in admin_ids_str.split(",")]
        return admin_ids
    except ValueError as e:
        raise ValueError(f"Invalid ADMIN_IDS format: {e}")


def get_channel_id() -> str:
    """Get channel ID from environment variables"""
    channel_id = os.getenv("CHANNEL_ID")
    if not channel_id:
        raise ValueError("CHANNEL_ID not found in .env file")
    return channel_id
