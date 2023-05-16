import requests
import logging
from telegram import __version__ as TG_VER
import azure.cognitiveservices.speech as speechsdk

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

speech_key = '205d9032223c4a68b5b4f06ccce5cc80f'
service_region = 'eastus'
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
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
            await update.message.reply_text("Üzgünüm, sorunuzu yanıtlayamıyorum.")
    except:
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

async def handle_voice_message(update: Update, context: CallbackContext):
    try:
        voice = update.message.voice  # Get the Voice object
        file_id = voice.file_id  # Get the unique file ID
        file = await context.bot.get_file(file_id)  # Get the file using the file ID
        file_bytes = await file.download_as_bytearray()  # Get the contents of the file as a byte array
        with open('voice_message.wav', 'wb') as f:
            f.write(file_bytes)  # Save the file contents to a file

        audio_config = speechsdk.AudioConfig(filename=  "../voice_message.wav")
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        result = speech_recognizer.recognize_once_async().get()
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            text = result.text
            print(text)
        else:
            text = 'Ses kaydınızı işlerken bir hata oluştu.'

        try:
            x = requests.get('http://metubot.ceng.metu.edu.tr/ask?question=' + text)
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
                await update.message.reply_text("Üzgünüm, sorunuzu yanıtlayamıyorum.")
        except:
            await update.message.reply_text("üzgünüm, sorunuzu yanıtlayamıyorum.")
    except:
        await update.message.reply_text("üzgünüm, sorunuzu yanıtlayamıyorum.")



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

    # VOICE
    application.add_handler(MessageHandler(filters.VOICE, handle_voice_message))

    # POLLING
    application.run_polling()


if __name__ == "__main__":
    main()