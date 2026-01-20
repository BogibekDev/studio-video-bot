"""
Main entry point - starts the Telegram bot
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import get_bot_token, get_admin_ids
from db.database import init_database
from handlers import admin, user


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Main function to start the bot"""
    # Initialize database
    logger.info("Initializing database...")
    init_database()
    logger.info("Database initialized")
    
    # Get bot token
    token = get_bot_token()
    admin_ids = get_admin_ids()
    logger.info(f"Bot starting with {len(admin_ids)} admin(s)")
    
    # Create bot and dispatcher
    bot = Bot(token=token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Register routers
    # Admin router should be registered first to handle admin commands
    dp.include_router(admin.router)
    dp.include_router(user.router)
    
    # Start polling
    logger.info("Bot started and polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
