import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# 🔹 Enable logging (for debugging on Render logs)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 🔹 Get token from environment variable (or paste directly if local)
TOKEN = os.getenv("BOT_TOKEN", "8308393313:AAG5GQKaFntuwx77zaTNBMKarkciAao1YhY")

# --- Basic command handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎯 Welcome! This is your Spin Bot. Type /spin to play!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ℹ️ Use /spin to try your luck!")

async def spin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import random
    prize = random.choice(["💎 10 points", "💰 50 coins", "🎁 Bonus spin", "😢 Try again!"])
    await update.message.reply_text(f"You spun the wheel and got: {prize}")

# --- Main function ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("spin", spin))

    logger.info("✅ Bot started successfully!")
    app.run_polling()

if __name__ == "__main__":
    main()
