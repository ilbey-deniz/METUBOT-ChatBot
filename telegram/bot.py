import requests
import logging
from telegram import __version__ as TG_VER


try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def request_answer(message):
    x = requests.get('http://metubot.ceng.metu.edu.tr/ask?question=' + message)
    data = (x.json()["data"])

    if type(data) == str:
        return data
    
    else:
        return "Sorunuzu cevaplayabilmek için yeterli bilgiye sahip değilim."



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bir soru sorun, onu cevaplamaya çalışacağım.")
    
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Merhaba {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )





async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(request_answer(update.message.text))


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6082456296:AAEMLY46A8JalqNEdCMEQj2pVk89ItF7Mfg").build()

    # COMMANDS
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # MESSAGES
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))

    # POLLING
    application.run_polling()


if __name__ == "__main__":
    main()