"""
Admin handlers - video upload functionality
"""
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from states.add_video import AddVideoStates
from services.video_service import save_video
from config import get_channel_id, get_admin_ids
from aiogram.exceptions import TelegramBadRequest


router = Router()
ADMIN_IDS = set(get_admin_ids())


def is_admin(user_id: int) -> bool:
    """Check if user is an admin"""
    return user_id in ADMIN_IDS


# Reply keyboard with "Add video" button
def get_admin_keyboard() -> ReplyKeyboardMarkup:
    """Create admin reply keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="➕ Add video")]],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard


@router.message(F.text == "/start", F.from_user.id.in_(ADMIN_IDS))
async def handle_start(message: Message):
    """Handle /start command - show keyboard for admins"""
    await message.answer(
        "➕ Add video tugmasini bosib, video yuboring.",
        reply_markup=get_admin_keyboard()
    )


@router.message(F.text == "➕ Add video", F.from_user.id.in_(ADMIN_IDS))
async def handle_add_video_button(message: Message, state: FSMContext):
    """
    Handle "Add video" button press
    Start FSM and ask admin to upload video
    """
    # Cancel any existing FSM state
    await state.clear()
    
    # Set state to waiting for video
    await state.set_state(AddVideoStates.waiting_for_video)
    
    await message.answer(
        "Bitta video yuboring.",
        reply_markup=get_admin_keyboard()
    )


@router.message(AddVideoStates.waiting_for_video, F.video, F.from_user.id.in_(ADMIN_IDS))
async def handle_video_upload(message: Message, state: FSMContext):
    """
    Handle video upload from admin
    Forward video to channel and ask for video ID
    """
    channel_id = get_channel_id()
    video = message.video
    file_id = video.file_id
    caption = message.caption or ""
    
    try:
        # Forward video to private channel
        forwarded = await message.forward(chat_id=channel_id)
        channel_message_id = forwarded.message_id
    except TelegramBadRequest as e:
        await message.answer(
            f"❌ Videoni kanalga yuborishda xatolik: {e}",
            reply_markup=get_admin_keyboard()
        )
        await state.clear()
        return
    
    # Store file_id temporarily in FSM state
    await state.update_data(file_id=file_id, caption=caption, channel_message_id=channel_message_id)
    
    # Change state to waiting for ID
    await state.set_state(AddVideoStates.waiting_for_id)
    
    await message.answer(
        "Video kanalga yuborildi. Videoning ID sini yuboring (masalan, 25.11.2022 yoki 25.11.2022.1).",
        reply_markup=get_admin_keyboard()
    )


@router.message(AddVideoStates.waiting_for_id, F.text, F.from_user.id.in_(ADMIN_IDS))
async def handle_video_id(message: Message, state: FSMContext):
    """
    Handle video ID input from admin
    Validate and save video to database
    """
    video_id = message.text.strip()
    state_data = await state.get_data()
    file_id = state_data.get("file_id")
    caption = state_data.get("caption", "")
    channel_message_id = state_data.get("channel_message_id", 0)
    
    if not file_id:
        await message.answer(
            "❌ Video topilmadi. Avval video yuboring.",
            reply_markup=get_admin_keyboard()
        )
        await state.clear()
        return
    
    try:
        # Save video using service layer
        save_video(video_id, file_id, caption, channel_message_id)
        
        await message.answer(
            f"✅ Video saqlandi. ID: {video_id}",
            reply_markup=get_admin_keyboard()
        )
    except ValueError as e:
        await message.answer(
            "❌ Video ID formati noto'g'ri. 25.11.2022 yoki 25.11.2022.1 ko'rinishida yuboring.",
            reply_markup=get_admin_keyboard()
        )
        return
    
    # Clear FSM state
    await state.clear()


@router.message(AddVideoStates.waiting_for_video, F.from_user.id.in_(ADMIN_IDS))
async def handle_invalid_video_input(message: Message, state: FSMContext):
    """Handle non-video messages when waiting for video"""
    if message.text == "➕ Add video":
        # Button pressed again, restart flow
        await handle_add_video_button(message, state)
    else:
        await message.answer(
            "Iltimos, video fayl yuboring.",
            reply_markup=get_admin_keyboard()
        )


@router.message(AddVideoStates.waiting_for_id, F.from_user.id.in_(ADMIN_IDS))
async def handle_invalid_id_input(message: Message, state: FSMContext):
    """Handle invalid input when waiting for video ID"""
    if message.text == "➕ Add video":
        # Button pressed again, restart flow
        await state.clear()
        await handle_add_video_button(message, state)
    elif message.video:
        # New video uploaded, restart flow
        await state.clear()
        await handle_video_upload(message, state)
    else:
        await message.answer(
            "Iltimos, to'g'ri video ID yuboring (masalan, 25.11.2022 yoki 25.11.2022.1).",
            reply_markup=get_admin_keyboard()
        )
