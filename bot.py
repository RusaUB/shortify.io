import logging
import re

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from shortify.config import TOKEN
from  shortify.sum_yt import generate_summary_from_youtube_video

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    message_text = update.message.text
    if is_youtube_link(message_text):
        video_id = extract_video_id(message_text)
        summary = generate_summary_from_youtube_video(video_id)
        await update.message.reply_text(summary)
    else:
        await update.message.reply_text(update.message.text)

def is_youtube_link(text):
    return re.match(r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]+(&\S*)?', text)

def extract_video_id(url):
    match = re.match(r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)(?P<id>[\w-]+)(&\S*)?', url)
    return match.group('id') if match else None

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
