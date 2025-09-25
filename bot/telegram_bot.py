import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import os
import zipfile
import subprocess

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load config
import config

# In-memory store for active shells and loot files (placeholders)
ACTIVE_SHELLS = {}
LOOT_FILES = []

# Helper: Check if user is admin
def is_admin(user_id):
    return user_id in config.ADMINS

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_markdown_v2(
        fr"Hello {user.mention_markdown_v2()}! Welcome to the Pentesting Bot.\n"
        "Use /scan <domain> to start full recon and exploit.\n"
        "Use /loot to get all gathered data zip.\n"
        "Use /shells to list active shells.\n"
        "Use /stats to see scan and proxy status.\n"
        "Admin commands: /admin, /update\n"
        "Ready to roll!"
    )

# /scan command
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("❌ You are not authorized to run this command.")
        return

    if not context.args:
        await update.message.reply_text("Please provide a domain. Usage:\n/scan example.com")
        return

    domain = context.args[0]
    await update.message.reply_text(f"🔍 Starting full scan pipeline for: {domain}")

    # TODO: Trigger your chain: proxy -> recon -> exploit -> dump -> shell
    # Example using subprocess to call sqlmap on target domain (expand this)
    # proc = subprocess.Popen(['sqlmap', '-u', f'http://{domain}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # out, err = proc.communicate()

# /loot command
async def loot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("❌ You are not authorized to run this command.")
        return

    if not LOOT_FILES:
        await update.message.reply_text("No loot available yet.")
        return

    zip_path = os.path.join(config.ZIP_OUTPUT_FOLDER, "loot_package.zip")

    # Create zip archive of loot files
    with zipfile.ZipFile(zip_path, 'w') as loot_zip:
        for file_path in LOOT_FILES:
            loot_zip.write(file_path, os.path.basename(file_path))

    # Send zip file
    with open(zip_path, 'rb') as file:
        await update.message.reply_document(file)
    await update.message.reply_text("📦 Loot package sent.")

# /shells command
async def shells(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("❌ You are not authorized to run this command.")
        return

    if not ACTIVE_SHELLS:
        await update.message.reply_text("No active reverse shells.")
        return

    response = "Active reverse shells:\n"
    for shell_id, shell_info in ACTIVE_SHELLS.items():
        response += f"{shell_id}: {shell_info}\n"
    await update.message.reply_text(response)

# /stats command
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("❌ Unauthorized.")
        return

    msg = (
        "📊 Bot Stats:\n"
        f"Max concurrent tasks: {config.MAX_CONCURRENT_TASKS}\n"
        f"Proxy rotation interval (s): {config.PROXY_ROTATION_INTERVAL}\n"
        f"Active shells: {len(ACTIVE_SHELLS)}\n"
        f"Loot files cached: {len(LOOT_FILES)}"
    )
    await update.message.reply_text(msg)

# /admin command
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in config.ADMINS:
        await update.message.reply_text("❌ Unauthorized.")
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage:\n"
            "/admin add <user_id> - Add admin\n"
            "/admin remove <user_id> - Remove admin"
        )
        return

    action = context.args[0].lower()
    try:
        target_id = int(context.args[1])
    except ValueError:
        await update.message.reply_text("User ID must be an integer.")
        return

    if action == "add":
        if target_id in config.ADMINS:
            await update.message.reply_text(f"User {target_id} is already admin.")
        else:
            config.ADMINS.append(target_id)
            await update.message.reply_text(f"Added admin: {target_id}")

    elif action == "remove":
        if target_id in config.ADMINS:
            config.ADMINS.remove(target_id)
            await update.message.reply_text(f"Removed admin: {target_id}")
        else:
            await update.message.reply_text(f"User {target_id} is not an admin.")
    else:
        await update.message.reply_text("Invalid action. Use add or remove.")

# /update command
async def update_plugins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("❌ Unauthorized.")
        return

    await update.message.reply_text("Updating plugins from GitHub...")
    # TODO: Call git commands or plugin loader update logic here
    # e.g., subprocess.run(["git", "pull"], cwd="path_to_plugin_folder")
    await update.message.reply_text("Plugins updated.")

# Handler for unknown commands
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Sorry, I didn't understand that command.\n"
        "Use /start to see available commands."
    )

def main():
    application = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("scan", scan))
    application.add_handler(CommandHandler("loot", loot))
    application.add_handler(CommandHandler("shells", shells))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("admin", admin))
    application.add_handler(CommandHandler("update", update_plugins))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))  # Unknown commands

    application.run_polling()

if __name__ == "__main__":
    main()
