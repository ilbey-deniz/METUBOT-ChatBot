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
from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters,  CallbackQueryHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    x = requests.get('http://metubot.ceng.metu.edu.tr/ask?question=' + update.message.text)
    data = (x.json()["data"])
    if type(data) == str:
        await update.message.reply_text(data)
    elif data[0]["type"]=="button" :
        button = []
        for i in range(len(data)):
            cb = data[i]["answer"][0]
            button.append([InlineKeyboardButton(data[i]["text"],callback_data=cb)])
        await context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(button),text="Lütfen seçiniz")
    else:
        await update.message.reply_text("üzgünüm, sorunuzu yanıtlayamıyorum.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bir soru sorun, onu cevaplamaya çalışacağım.")
    
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Merhaba {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def queryHandler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    print(query)
    
    await context.bot.send_message(chat_id=update.effective_chat.id,text=query)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6082456296:AAEMLY46A8JalqNEdCMEQj2pVk89ItF7Mfg").build()

    # COMMANDS
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # MESSAGES
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))

    # QUERY
    application.add_handler(CallbackQueryHandler(queryHandler))

    # POLLING
    application.run_polling()


if __name__ == "__main__":
    main()