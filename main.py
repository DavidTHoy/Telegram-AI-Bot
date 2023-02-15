import html
import json
import logging
import os
import traceback

import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CallbackContext, CommandHandler

from ai_service import AiService
from helper_functions import get_request_headers, get_data_from_html

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


async def error_handler(update: object, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )
    await context.bot.send_message(
        chat_id=os.getenv('DEVELOPER_CHAT_ID'), text=message, parse_mode=ParseMode.HTML
    )


async def tldr(update: Update, context: CallbackContext):
    logger.info(f'Getting tldr for {context.args[0]}')
    try:
        r = requests.get(context.args[0], headers=get_request_headers())
        if not r.status_code == 200:
            await update.message.reply_text("Received non 200 status for article")
            return
        outputs = AiService.summarize_text(get_data_from_html(r.text))
        await update.message.reply_text(text=outputs, parse_mode=ParseMode.HTML)
    except Exception as e:
        await update.message.reply_text(str(e))


async def pic(update: Update, context: CallbackContext):
    logger.info(*context.args)
    image = AiService.generate_image(''.join(context.args), num_images=3, guidance_scale=5, num_inference_steps=30)
    image.save("latest.png")
    # Could use the below if graphics card has enough memory, so you don't have to save to disk
    # buf = io.BytesIO()
    # image.save(buf, format='png')
    # byte_im = buf.getvalue()
    # update.message.reply_photo(byte_im)
    with open("latest.png", 'rb') as f:
        await update.message.reply_photo(f)


if __name__ == '__main__':
    token = os.getenv('TELEGRAM_API_KEY', '')
    application = Application.builder().token(token).build()

    # application.add_handler(CommandHandler('pic', pic))
    application.add_handler(CommandHandler('tldr', tldr))
    application.add_error_handler(error_handler)
    application.run_polling()
