# Telegram Video Bot

A Telegram bot built with aiogram 3 for managing and retrieving videos by ID.

## Features

- **Admin video upload**: Admins can upload videos via Reply Keyboard button
- **Video forwarding**: Videos are automatically forwarded to a private channel
- **ID-based retrieval**: Users can request videos by providing an ID
- **Multiple videos per ID**: Support for multiple videos with the same ID
- **ID validation**: Strict validation for video IDs (e.g., 25.11.2022, 25.11.2022.1)

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:
   - Copy `.env.example` to `.env`
   - Fill in your bot token, admin IDs, and channel ID

3. **Run the bot**:
   ```bash
   python main.py
   ```

## Environment Variables

- `BOT_TOKEN`: Your bot token from @BotFather
- `ADMIN_IDS`: Comma-separated list of admin Telegram user IDs
- `CHANNEL_ID`: Private channel ID where videos will be forwarded

## Usage

### Admin Flow

1. Press the "➕ Add video" button in the Reply Keyboard
2. Upload a video file
3. Provide a video ID (e.g., `25.11.2022` or `25.11.2022.1`)
4. Video is saved and forwarded to the channel

### User Flow

1. Send a video ID to the bot (e.g., `25.11.2022`)
2. Receive all videos associated with that ID

## Project Structure

```
bot/
 ├── main.py                 # Entry point
 ├── config.py               # Environment configuration
 ├── db/
 │   ├── database.py         # SQLite connection
 │   └── video_repo.py       # Database operations
 ├── services/
 │   ├── video_service.py    # Business logic
 │   └── validation.py       # ID validation
 ├── handlers/
 │   ├── admin.py            # Admin handlers
 │   └── user.py             # User handlers
 ├── states/
 │   └── add_video.py        # FSM states
 ├── middlewares/
 │   └── admin_only.py       # Admin middleware
 └── data/
     └── videos.db           # SQLite database
```
