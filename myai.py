import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Set up Telegram bot token
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Set up Gemini API key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro-exp-0827')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['chat'] = model.start_chat(history=[])
    await update.message.reply_text('Hello! I am your AI assistant powered by Gemini. How can I help you today?')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        if 'chat' not in context.user_data:
            context.user_data['chat'] = model.start_chat(history=[])
        
        chat = context.user_data['chat']
        response = chat.send_message(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        await update.message.reply_text(f"Sorry, I couldn't process your request. Please try again later. Error: {str(e)}")

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['chat'] = model.start_chat(history=[])
    await update.message.reply_text("Chat history has been cleared. Let's start a new conversation!")

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("clear", clear))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
