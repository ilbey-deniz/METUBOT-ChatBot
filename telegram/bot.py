import requests
import logging
from telegram import __version__ as TG_VER
import azure.cognitiveservices.speech as speechsdk
import soundfile as sf
import librosa

button_answer = {}
api2 = "21676b8af2a44a35a6d397ebe9bd23db"
api_key = "205d9032223c4a68b5b4f06cce5cc80f" 
region="eastus"
speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region, speech_recognition_language="tr-TR")

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
from telegram import ForceReply, Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters,  CallbackQueryHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def send_voice(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    audio_path = "telegram/output.wav"
    audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_path)
    speech_config.speech_synthesis_language = "tr-TR"
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized to speaker for text [{}]".format(text))
        await update.message.reply_voice(open(audio_path, "rb"))
    elif result.reason == speechsdk.ResultReason.Canceled:
        await update.message.reply_text("Ses sentezleme iptal edildi.")
    else:
        await update.message.reply_text("Ses sentezleme başarısız oldu.")

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text(button_answer[update.message.text])
        return
    except KeyError:
        button_answer.clear()

    #try:
        x = requests.get('http://metubot.ceng.metu.edu.tr/ask?question=' + update.message.text)
        data = x.json()["data"]
        print(data)
        if type(data) == str:
            await update.message.reply_text(data)
            await send_voice(update, context, data)
        elif data[0]["type"]=="button" :
            buttons = []
            for i in range(len(data)):
                button = KeyboardButton(data[i]["text"])
                buttons.append([button])
                button_answer[data[i]["text"]] = data[i]["answer"][0] 
            print(buttons)
            reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            await update.message.reply_text('Lütfen Seçiniz', reply_markup=reply_markup)
        else:
            await update.message.reply_text("Üzgünüm, sorunuzu yanıtlayamıyorum.")
    #except:
        #await update.message.reply_text("Üzgünüm, sorunuzu yanıtlayamıyorum.")

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

def recognize_speech(path):

    audio_config = speechsdk.audio.AudioConfig(filename=path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config, audio_config)
    result = speech_recognizer.recognize_once()

    # Check the recognition result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "Ses algılanamadı."
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speechsdk.CancellationDetails(result)
        print(f"Cancellation reason: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Cancellation error details: {cancellation_details.error_details}")
        return "Algılama iptal edildi veya tamamlanamadı."


async def handle_voice_message(update: Update, context: CallbackContext):
    try:
        message = update.effective_message
        path = 'telegram/voice_message_raw.wav'
        file = await message.voice.get_file()
        filebytes = await file.download_as_bytearray()
        with open(path, 'wb') as f:
            f.write(filebytes)
        y, s = librosa.load(path, sr=16000)
        path = 'telegram/voice_message.wav'
        sf.write(path, y, s)

        text = recognize_speech(path)
        
        if text == "Ses algılanamadı." or text == "Algılama iptal edildi veya tamamlanamadı.":
            await update.message.reply_text(text)
        else:
            x = requests.get('http://metubot.ceng.metu.edu.tr/ask?question=' + text)
            data = (x.json()["data"])
            if type(data) == str:
                await update.message.reply_text(data)
            elif data[0]["type"]=="button" :
                buttons = []
                for i in range(len(data)):
                    button = KeyboardButton(data[i]["text"])
                    buttons.append([button])
                    button_answer[data[i]["text"]] = data[i]["answer"][0] 
                print(buttons)
                reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
                await update.message.reply_text('Lütfen Seçiniz', reply_markup=reply_markup)
            else:
                await update.message.reply_text("Üzgünüm, sorunuzu yanıtlayamıyorum.")
    except:
        await update.message.reply_text("Üzgünüm, sorunuzu yanıtlayamıyorum.")



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