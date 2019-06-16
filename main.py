


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
import youtube_dl
import os
from logzero import logger
from path import Path


TOKEN = os.environ.get('TOKEN')
# ----------------------- YT-dl part --------------------------

class MyLogger(object):
    def debug(self, msg):
        loger.debug("yt-dl: {}".format(msg))

    def warning(self, msg):
        loger.warning("yt-dl: {}".format(msg))

    def error(self, msg):
        loger.error("yt-dl: {}".format(msg))


def filename_to_mp3(filename):
    return os.path.splitext(filename)[0] + ".mp3"


ydl_mp3_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "logger": MyLogger(),
        
    }

def search_youtube_to_mp3(query):
    """
    save the the mp3 for the first yt video found with the search query
    """
    return youtube_to_mp3("ytsearch1:{}".format(query))

def youtube_to_mp3(url):
    """
    save the the mp3 for the yt url provided
    """
    filename_mut = []
    def save_filename(d):
        if d["status"] == "finished":
            logger.info("yt-dl: Done downloading '{}', now converting ...".format(d["filename"]))
            filename_mut.append(d["filename"])

    opts = ydl_mp3_opts
    # add the hook
    opts["progress_hooks"] = [save_filename]

    with youtube_dl.YoutubeDL(ydl_mp3_opts) as ydl:
        ydl.download([url])
    
    # finish processing
    if len(filename_mut) > 0:
        return filename_to_mp3(filename_mut[0])
    
    return ""


# ---------------------------- TL bot part ----------------------------------

def help(bot, update):
    """Send a message when the command /help is issued."""
    logger.info('Received /help command from %s' % update.message.from_user.username)
    update.message.reply_text('Send you an mp3 from the youtube video find with the string')

def yt_dl(bot, update):
    """
    launch yt-dl for the given string (differentiate url from string search)
    """

    filename = "youtube-dl test video ''_ä↭𝕐-BaW_jenozKc.mp3"
    p = Path(filename)
    if p.exists():
        # update.message.reply_text("ok")
        update.message.reply_audio(audio=open(p.realpath(), 'rb'))
    else:
        update.message.reply_text("Fail")

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.info("Entered in error function")
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

   
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("yt_dl", yt_dl))


    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, bonne_annee))
    # log all errors
    dp.add_error_handler(error)




    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    logger.info("yt-dl bot is launched !")
    updater.idle()
    logger.info("yt-dl bot stopped")

if __name__ == '__main__':
    main()