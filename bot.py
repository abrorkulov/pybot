import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
    exit(1)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        '👋 Welcome to the YouTube Video Downloader Bot!\n\n'
        'Send me a YouTube link and I will download the video for you.\n\n'
        'Commands:\n'
        '/start - Start the bot\n'
        '/help - Show help message'
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        '📖 Help:\n\n'
        'Simply send me a YouTube URL and I will download the video for you.\n\n'
        'Supported formats:\n'
        '- YouTube videos\n'
        '- YouTube shorts\n'
        '- Other video platforms supported by yt-dlp\n\n'
        'The bot will send you the best quality video available.'
    )


async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Download video from YouTube URL."""
    url = update.message.text
    
    # Check if it's a command
    if url.startswith('/'):
        return
    
    logger.info(f"Received URL: {url}")
    
    # Send processing message
    status_message = await update.message.reply_text('⏳ Processing your request...')
    
    try:
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
        }
        
        # Create downloads directory if it doesn't exist
        os.makedirs('downloads', exist_ok=True)
        
        # Download video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await status_message.edit_text('📥 Downloading video...')
            info = ydl.extract_info(url, download=True)
            
            video_title = info.get('title', 'video')
            video_ext = info.get('ext', 'mp4')
            video_filename = f"downloads/{video_title}.{video_ext}"
            
            logger.info(f"Downloaded: {video_filename}")
            
            # Check if file exists and is not too large (Telegram limit is 50MB)
            file_size = os.path.getsize(video_filename)
            max_size = 50 * 1024 * 1024  # 50MB
            
            if file_size > max_size:
                await status_message.edit_text(
                    f'❌ Video is too large ({file_size/1024/1024:.1f}MB). '
                    f'Telegram limit is 50MB. '
                    f'Please try a shorter video.'
                )
                # Clean up
                os.remove(video_filename)
                return
            
            # Send video to user
            await status_message.edit_text('📤 Uploading video...')
            with open(video_filename, 'rb') as video_file:
                await update.message.reply_video(
                    video_file,
                    caption=f'🎬 {video_title}',
                    read_timeout=60,
                    write_timeout=60
                )
            
            await status_message.edit_text('✅ Video sent successfully!')
            
            # Clean up
            os.remove(video_filename)
            logger.info(f"Cleaned up: {video_filename}")
            
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        await status_message.edit_text(
            f'❌ Error downloading video: {str(e)}\n\n'
            f'Make sure the URL is valid and the video is accessible.'
        )


def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    
    # Start the bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
