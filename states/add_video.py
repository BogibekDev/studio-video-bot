"""
FSM states for admin video upload flow
"""
from aiogram.fsm.state import State, StatesGroup


class AddVideoStates(StatesGroup):
    """FSM states for adding a video"""
    waiting_for_video = State()  # Waiting for admin to upload video
    waiting_for_id = State()     # Waiting for admin to provide video ID
