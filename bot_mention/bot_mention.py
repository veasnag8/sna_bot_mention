from telegram import Update
from telegram.ext import Application, MessageHandler, filters
from telegram.helpers import mention_html

# Initialize the bot with your token
TOKEN = "6743612662:AAFiKelfeEFxNTGQRORImQmbYocCPeisuC0"
app = Application.builder().token(TOKEN).build()

# List of prohibited words
PROHIBITED_WORDS = ["fuck", "site"]

# Function to handle messages and check for prohibited words or @allknea mention
async def handle_message(update: Update, context):
    message = update.message

    # Check for prohibited words
    if any(word.lower() in message.text.lower() for word in PROHIBITED_WORDS):
        await message.delete()  # Delete the message
        await context.bot.send_message(
            chat_id=message.chat_id,
            text="Inappropriate language is not allowed. Your message has been removed."
        )
        return

    # Check if the message contains "@allknea" to mention all members
    if "@allknea" in message.text.lower():
        # Fetch all chat members and construct the mention message
        members = await context.bot.get_chat_administrators(message.chat_id)
        mentions = " ".join(mention_html(user.user.id, user.user.first_name) for user in members)
        
        # Send a message mentioning all members
        await context.bot.send_message(
            chat_id=message.chat_id,
            text=f"Attention: {mentions}",
            parse_mode="HTML"
        )

# Add the message handler
app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.Document.ALL, handle_message))

# Start the bot
app.run_polling()
