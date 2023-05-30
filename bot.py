import logging
import asyncio
import requests
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, InlineQueryHandler
import os
from extractor import extract
import os

TOKEN = os.getenv('BOTAPIKEY')
PORT = int(os.environ.get('PORT', '443'))
HOOK_URL = 'YOUR-CODECAPSULES-URL-HERE' + '/' + TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usermsg = update.message.text
    reply = usermsg

    if "www.hk01.com/" in usermsg:
        reply = '01狗'
        requests.head("https://www.hk01.com/")
        if extract(usermsg):
            reply=extract(usermsg)
        else:
            reply="Article empty!"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

#async def inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #query = update.inline_query.query
    #if not query:
        #return
    #results = []
    #results.append(
        #InlineQueryResultArticle(
            #id=query,
            #title='抽出內文',
            #input_message_content=InputTextMessageContent(extractor.extract(query))
        #)
    #)
    #await context.bot.answer_inline_query(update.inline_query.id, results)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def main():
    loop = asyncio.get_event_loop()

    if loop.is_running():
        print("An event loop is already running.")
    else:
        loop.run_until_complete(asyncio.sleep(0))  # Start the event loop

    application = ApplicationBuilder().token(TOKEN).build()

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    #inline_handler = InlineQueryHandler(inline)
    #application.add_handler(inline_handler)

    # Other handlers
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_webhook(
    listen="0.0.0.0",
    port=PORT, url_path=TOKEN, webhook_url=HOOK_URL
    )

    application.get_webhook_info()

    #application.run_polling()

if __name__ == '__main__':
    main()