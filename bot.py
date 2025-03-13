import os
import asyncio
from rembg import remove
from PIL import Image
from io import BytesIO
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TELEGRAM_BOT_TOKEN

# Get PORT from environment variables (for deployment)
PORT = int(os.getenv("PORT", 5000))
WEBHOOK_URL = "https://your-deployment-url.com/"  # Replace with your actual webhook URL

# Function to remove background
def remove_background(image_data):
    try:
        input_image = Image.open(BytesIO(image_data)).convert("RGBA")  
        output_image = remove(input_image)

        img_byte_arr = BytesIO()
        output_image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)
        return img_byte_arr
    except Exception as e:
        print(f"Error removing background: {e}")
        return None

# Start command
async def start(update: Update, context):
    await update.message.reply_text("👋 Send me an image, and I'll remove the background!")

# Handle received images
async def handle_photo(update: Update, context):
    photo = update.message.photo[-1]  
    file = await context.bot.get_file(photo.file_id)
    image_bytes = await file.download_as_bytes()

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

    # For deployment using webhooks
    await app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL + TELEGRAM_BOT_TOKEN
    )

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())
