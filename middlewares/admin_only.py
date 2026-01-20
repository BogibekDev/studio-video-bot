"""
Admin-only middleware - checks if user is an admin
"""
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from config import get_admin_ids


class AdminOnlyMiddleware(BaseMiddleware):
    """Middleware to check if user is an admin"""
    
    def __init__(self):
        super().__init__()
        self.admin_ids = get_admin_ids()
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """Check if user is admin before processing handler"""
        # Get user ID from event
        user_id = None
        if hasattr(event, 'from_user') and event.from_user:
            user_id = event.from_user.id
        elif hasattr(event, 'message') and event.message and event.message.from_user:
            user_id = event.message.from_user.id
        
        if user_id and user_id in self.admin_ids:
            return await handler(event, data)
        else:
            # Not an admin, skip handler
            return None
