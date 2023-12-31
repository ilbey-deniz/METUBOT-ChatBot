import requests
import logging
from telegram import __version__ as TG_VER
import azure.cognitiveservices.speech as speechsdk
import soundfile as sf
from random import choice
import librosa

local = "http://localhost:3000/ask?question="
server = "http://metubot.ceng.metu.edu.tr/ask?question="

all_button_answer = {}
ses = {}
api_key = "c8f16b9dfc984870afa3dc696e6fdc39"  
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
        await update.message.reply_text(all_button_answer[update.effective_chat.id][update.message.text])
        try:
            if ses[update.message.chat_id] == True:
                await send_voice(update, context, all_button_answer[update.effective_chat.id][update.message.text])
        except KeyError:
            pass
        return
    except KeyError:
        try:
            all_button_answer.pop(update.effective_chat.id)
        except KeyError:
            pass

    try:
        x = requests.get(server + update.message.text)
        data = x.json()["data"]
        print(data)
        if len(data["buttons"]) == 0:
            ret = choice(data["answer"])
            await update.message.reply_text(ret)
            try:
                if ses[update.message.chat_id] == True:
                    await send_voice(update, context, ret)
            except KeyError:
                pass
        elif len(data["buttons"]) > 0:
            buttons = []
            button_answer = {}
            for i in range(len(data["buttons"])):
                button = KeyboardButton(data["buttons"][i]["text"])
                buttons.append([button])
                button_answer[data["buttons"][i]["text"]] = data["buttons"][i]["answer"][0] 
            all_button_answer[update.effective_chat.id] = button_answer
            print(buttons)
            reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
            await update.message.reply_text(data["answer"][0], reply_markup=reply_markup)
        else:
            await update.message.reply_text("Üzgünüm, sorunuzu yanıtlayamıyorum.")
    except:
        await update.message.reply_text("Üzgünüm, sorunuzu yanıtlayamıyorum.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("/ses komutu sesli yanıtı açar/kapatır.")

async def manage_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        ses[update.message.chat_id]
    except KeyError:
        ses[update.message.chat_id] = False

    if ses[update.message.chat_id] == False:
        ses[update.message.chat_id] = True
        await update.message.reply_text("Sesli yanıt aktif edildi.")
        
    else:
        ses[update.message.chat_id] = False
        await update.message.reply_text("Sesli yanıt deaktif edildi.")
        
    
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ses[update.message.chat_id] = False
    user = update.effective_user
    await update.message.reply_html(
        rf"Merhaba {user.mention_html()}, ben METUBOT! Size nasıl yardımcı olabilirim? \n /ses komutu sesli yanıtı açar/kapatır.",
    )
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
        print(f"İptal sebebi: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"İptal sebebi detayları: {cancellation_details.error_details}")
        return "Algılama iptal edildi veya tamamlanamadı."


async def handle_voice_message(update: Update, context: CallbackContext):
    try:
        all_button_answer.pop(update.effective_chat.id)
    except KeyError:
        pass
    
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
            x = requests.get(server + text)
            data = x.json()["data"]
            if len(data["buttons"]) == 0:
                    ret = choice(data["answer"])
                    await update.message.reply_text(ret)
                    try:
                        if ses[update.message.chat_id] == True:
                            await send_voice(update, context, ret)
                    except KeyError:
                        pass
            elif len(data["buttons"]) > 0:
                buttons = []
                button_answer = {}
                for i in range(len(data["buttons"])):
                    button = KeyboardButton(data["buttons"][i]["text"])
                    buttons.append([button])
                    button_answer[data["buttons"][i]["text"]] = data["buttons"][i]["answer"][0] 
                all_button_answer[update.effective_chat.id] = button_answer
                print(buttons)
                reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
                await update.message.reply_text(data["answer"][0], reply_markup=reply_markup)
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
    application.add_handler(CommandHandler("ses", manage_voice))
    # MESSAGES
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))

    # VOICE
    application.add_handler(MessageHandler(filters.VOICE, handle_voice_message))

    # POLLING
    application.run_polling()


if __name__ == "__main__":
    main()