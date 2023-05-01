import os
from telegram.ext import Updater, MessageHandler, Filters
import openai

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set Telegram bot token
updater = Updater(token=os.getenv("TELEGRAM_BOT_TOKEN"), use_context=True)

# Define your GPT prompt here
prompt = "Ask me anything!"

# Define function to generate GPT response
def generate_response(input_text):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt + input_text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response.choices[0].text
    return message.strip()

# Define handler function to respond to user messages
def handle_message(update, context):
    input_text = update.message.text
    if "@" in input_text and "@your_bot_username" in input_text:
        # Remove bot mention from message
        input_text = input_text.replace("@your_bot_username", "").strip()
        response = generate_response(input_text)
        update.message.reply_text(response)

# Set up message handler and start the bot
updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
updater.start_polling()
updater.idle()
