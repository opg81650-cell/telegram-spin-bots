import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ✅ Load the bot token safely from environment variables
TOKEN = os.environ.get("TG_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("Bot token not found! Please set TG_BOT_TOKEN in Render environment.")

# 🎯 Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎡 Welcome to Spin Wheel Bot!\n\nType /spin to try your luck 🎯"
    )

# 🎡 Spin command
async def spin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prizes = ["₹10", "₹50", "₹100", "₹250", "₹500", "₹1000", "Better luck next time!"]
    result = random.choice(prizes)
    await update.message.reply_text(f"🎉 You spun the wheel and won: {result}")

# 🚀 Main app
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("spin", spin))

    print("✅ Bot started successfully... Listening for spins 🎡")
    app.run_polling()

if __name__ == "__main__":
    main()
