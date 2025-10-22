# main.py
# Requirements: python-telegram-bot==20.0
# A simple spin-wheel bot (demo). Use environment variable TG_BOT_TOKEN in Replit/Render.

import os
import random
import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Get token from environment variable - safer than pasting directly in code
TOKEN = os.getenv("8308393313:AAG5GQKaFntuwx77zaTNBMKarkciAao1YhY")
if not TOKEN:
    import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Get token from environment variable
TOKEN = os.environ.get("8308393313:AAG5GQKaFntuwx77zaTNBMKarkciAao1YhY")

if not TOKEN:
    raise RuntimeError("8308393313:AAG5GQKaFntuwx77zaTNBMKarkciAao1YhY. 8308393313:AAG5GQKaFntuwx77zaTNBMKarkciAao1YhY in Render environment.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎡 Welcome to Spin Wheel Bot!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("✅ Bot started successfully...")
app.run_polling()

# --- Database setup (sqlite) ---
conn = sqlite3.connect("data.db", check_same_thread=False)
conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 0,
    spins INTEGER DEFAULT 1,
    referred_by INTEGER
)
""")
conn.commit()

def add_user(user_id: int, ref: int | None = None):
    existing = conn.execute("SELECT id FROM users WHERE id=?", (user_id,)).fetchone()
    if existing:
        return
    conn.execute("INSERT INTO users (id, referred_by) VALUES (?, ?)", (user_id, ref))
    conn.commit()

# --- Command handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    ref = int(args[0]) if args else None
    add_user(user_id, ref)
    text = (
        "🎡 Welcome to Lucky Spin Bot!\n\n"
        "Commands:\n"
        "/spin - Use one spin to win coins\n"
        "/balance - See your balance and spins left\n"
        "/invite - Get your referral link to earn spins\n\n"
        "Good luck!"
    )
    await update.message.reply_text(text)

async def spin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    row = conn.execute("SELECT spins, balance FROM users WHERE id=?", (user_id,)).fetchone()
    if not row:
        await update.message.reply_text("Please send /start first.")
        return
    spins, balance = row
    if spins <= 0:
        await update.message.reply_text("You have no spins left. Invite friends with /invite to earn spins.")
        return

    # You can change prizes here:
    prizes = [0, 5, 10, 20, 50, 100]   # 0 means no win
    prize = random.choice(prizes)

    conn.execute("UPDATE users SET spins = spins - 1, balance = balance + ? WHERE id = ?", (prize, user_id))
    conn.commit()

    if prize == 0:
        await update.message.reply_text("😞 No luck this time. Try again later!")
    else:
        await update.message.reply_text(f"🎉 Congratulations — you won {prize} coins!")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    row = conn.execute("SELECT balance, spins FROM users WHERE id=?", (user_id,)).fetchone()
    if not row:
        await update.message.reply_text("Please send /start first.")
        return
    balance, spins = row
    await update.message.reply_text(f"💰 Balance: {balance} coins\n🎡 Spins left: {spins}")

async def invite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bot_username = (await context.bot.get_me()).username
    link = f"https://t.me/{bot_username}?start={user_id}"
    await update.message.reply_text(f"Invite friends with this link:\n{link}\nWhen they join with this link you (optionally) get +1 spin.")

# --- Start bot (polling: easy for testing / Replit) ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("spin", spin))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("invite", invite))
    print("Bot started. Listening for updates...")
    app.run_polling()

if __name__ == "__main__":
    main()
