# -*- coding: utf-8 -*- 
import logging
import os
from pathlib import Path
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import cv2
import sys
import subprocess
from time import sleep
import random

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

cur_dir = Path('.')
cur_dir = cur_dir.resolve()

def start(update,context):
    update.message.reply_text('Hi!')


def help(update,context):
    update.message.reply_text('Help!')


def echo(update,context):
    update.message.reply_text(update.message.text)

def get_photo(update,context) :
    global cur_dir
    file_path = os.path.join(cur_dir, 'from_telegram.jpg')
    photo_id = update.message.photo[-1].file_id  
    photo_file = context.bot.getFile(photo_id)
    photo_file.download(file_path)
    #update.message.reply_text('photo saved')
    sleep(0.5)
    subprocess.call(['python3', 'sudoku.py'])
    sleep(0.5)
    f = open('sol.txt','r')
    lines = f.read()
    sleep(1)
    update.message.reply_text(lines)

def send_sk(update,context):
    global cur_dir
    fpath = 'smu.jpg'
    print(fpath)
    flist = [str(x) for x in cur_dir.iterdir() if not x.is_dir()]

    for item in flist:
        if fpath in item:
            fk = open(item, "rb")
            context.bot.send_document(chat_id=update.message.chat_id, document=fk)
            break

def _list(update,context):
    global cur_dir
    pl = [str(x) for x in cur_dir.iterdir()]
    pl = "\n".join(pl)
    update.message.reply_text(pl)

def _parent(update,context):
    global cur_dir
    cur_dir = cur_dir.parent
    _list(update,context)

def _select(update,context):
    global cur_dir
    fpath = str(update.message.text).split()
    # fpath[0] : /select
    # fpath[1] : destination
    flist = [str(x) for x in cur_dir.iterdir() if x.is_dir()]

    for item in flist:
        if fpath[1] in item:
            cur_dir = Path(item)
            cur_dir = cur_dir.resolve()
            break

def _send(update,context):
    global cur_dir
    fpath = str(update.message.text).split()
    flist = [str(x) for x in cur_dir.iterdir() if not x.is_dir()]

    for item in flist:
        if fpath[1] in item:
            f = open(item, "rb")
            context.bot.send_document(chat_id=update.message.chat_id, document=f)
            break

def _img(update,context):
    global cur_dir
    pass
    

def _create(update,context):
    global cur_dir
    fpath = str(update.message.text).split()
    os.mkdir(str(cur_dir) + "/" + str(fpath[1]) + "/")

def _delete(update,context):
    global cur_dir
    fpath = str(update.message.text).split()
    os.rmdir(str(cur_dir) + "/" + str(fpath[1]))

def _rename(update,context):
    global cur_dir
    fpath = str(update.message.text).split()
    os.rename(str(cur_dir) + "/" + str(fpath[1]), str(cur_dir) + "/" + str(fpath[2]))

def _remove(update,context):
    global cur_dir
    fpath = str(update.message.text).split()
    os.remove(str(cur_dir) + "/" + str(fpath[1]))

def error(update,context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update,context.error)

def main():
    updater = Updater("759763304:AAHWYLXjzm0O3YorgFLE4Bvgy41wC14K-0k",use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("list", _list))
    dp.add_handler(CommandHandler("parent", _parent))
    dp.add_handler(CommandHandler("select", _select))
    dp.add_handler(CommandHandler("send", _send))
    dp.add_handler(CommandHandler("create", _create))
    dp.add_handler(CommandHandler("delete", _delete))
    dp.add_handler(CommandHandler("rename", _rename))
    dp.add_handler(CommandHandler("remove", _remove))
    dp.add_handler(CommandHandler("send_sk", send_sk))
    dp.add_handler(MessageHandler(Filters.photo, get_photo))
    

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()