import os
import asyncio
import nest_asyncio  
from rembg import remove
from PIL import Image
from io import BytesIO
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TELEGRAM_BOT_TOKEN  # Import bot token from config.py

nest_asyncio.apply()

# Function to remove background
def remove_background(image_data):
    try:
        input_image = Image.open(BytesIO(image_data))
        output_image = remove(input_image)

        # Convert output image to bytes
        img_byte_arr = BytesIO()
        output_image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        return img_byte_arr
    except Exception as e:
        print(f"Error: {e}")
        return None

# Start command
async def start(update: Update, context):
    await update.message.reply_text("👋 Send me an image, and I'll remove the background!")

# Handle received images
async def handle_photo(update: Update, context):
    photo = update.message.photo[-1]  # Get the highest quality image
    file = await context.bot.get_file(photo.file_id)
    image_bytes = await file.download_as_bytearray()

    # Remove background
    output_image = remove_background(image_bytes)

    if output_image:
        await update.message.reply_photo(photo=output_image, caption="✅ Background Removed!")
    else:
        await update.message.reply_text("❌ Failed to process the image.")

# Main function to run the bot
async def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("🤖 Bot is running...")
    await app.run_polling()

# Proper event loop handling
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())  # Correct way to start the bot
