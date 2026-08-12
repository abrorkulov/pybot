# YouTube Video Downloader Telegram Bot

A Telegram bot that allows users to download videos from YouTube and other supported platforms.

## Features

- Download YouTube videos by sending a URL
- Support for YouTube Shorts and other video platforms
- Automatic quality selection (best MP4 format)
- File size checking (Telegram 50MB limit)
- User-friendly commands and status updates

## Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (get it from [@BotFather](https://t.me/botfather))

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

4. Edit the `.env` file and add your Telegram bot token:
```
TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
```

## Getting a Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send the command `/newbot`
3. Follow the instructions to create your bot
4. Copy the bot token provided by BotFather
5. Paste it into your `.env` file

## Usage

Run the bot:
```bash
python bot.py
```

## Commands

- `/start` - Start the bot and see welcome message
- `/help` - Show help information

## How to Use

1. Start the bot by sending `/start`
2. Simply paste a YouTube URL in the chat
3. The bot will download and send the video to you
4. Wait for the download and upload to complete

## Supported Platforms

The bot uses `yt-dlp` which supports many video platforms including:
- YouTube
- YouTube Shorts
- Vimeo
- TikTok
- And many more

## Limitations

- Maximum file size: 50MB (Telegram limit)
- Download speed depends on your internet connection
- Some videos may be restricted or unavailable in your region

## Troubleshooting

**Bot doesn't respond:**
- Check that your bot token is correct in the `.env` file
- Ensure the bot is running without errors
- Make sure you've started a conversation with the bot in Telegram

**Download fails:**
- Verify the URL is valid and accessible
- Check your internet connection
- Some videos may be age-restricted or region-locked

**File too large error:**
- Telegram has a 50MB file size limit for bots
- Try downloading shorter videos or lower quality versions

## Project Structure

```
.
├── bot.py              # Main bot application
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .env                # Your actual environment variables (not in git)
├── downloads/          # Temporary download directory (auto-created)
└── README.md          # This file
```

## Dependencies

- `python-telegram-bot` - Telegram Bot API wrapper
- `yt-dlp` - YouTube video downloader
- `python-dotenv` - Environment variable management

## License

This project is open source and available for educational purposes.
