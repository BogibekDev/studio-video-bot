"""
User handlers - video request by ID functionality
"""
from aiogram import Router, F
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from services.video_service import get_videos
from config import get_admin_ids
from config import get_channel_id


router = Router()


def is_admin(user_id: int) -> bool:
    """Check if user is an admin"""
    return user_id in get_admin_ids()


@router.message(F.text == "/start")
async def handle_start(message: Message):
    """Handle /start command for regular users"""
    if is_admin(message.from_user.id):
        return
    await message.answer("To'y sanasini kiriting (masalan, 25.11.2022) ")


@router.message(F.text)
async def handle_user_request(message: Message):
    """
    Handle user video request by ID
    Send all videos associated with the provided ID
    """
    # Skip admin messages (they use admin handlers)
    if is_admin(message.from_user.id):
        return
    
    # Skip button presses and commands
    if message.text in ["➕ Add video", "/start"]:
        return
    
    video_id = message.text.strip()
    
    # Get videos from service layer
    videos = get_videos(video_id)
    
    if not videos:
        await message.answer("❌ Bu sana bo'yicha videolar topilmadi")
        return
    
    # Send each video one by one
    channel_id = get_channel_id()
    for video in videos:
        channel_message_id = video.get("channel_message_id") or 0
        if not channel_message_id:
            # Skip legacy entries without channel message linkage
            continue
        try:
            if channel_message_id:
                # Try copying from the channel; if deleted this will fail
                await message.bot.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=channel_id,
                    message_id=channel_message_id
                )
        except TelegramBadRequest:
            # Video not accessible (deleted/expired) -> skip
            await message.answer("❌ Bu sana bo'yicha videolar topilmadi. Studiomizga murojaat qiling.")
            continue
