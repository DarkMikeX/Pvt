import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Telegram Bot configuration
TELEGRAM_TOKEN = "8359242986:AAHTHZtAxjv09MPXjj4cmE1lZoHxOAKcJUA"

# Telegram user IDs with admin privileges (replace as needed)
ADMINS = [6447766151]

# Pentesting tool paths (relative to BASE_DIR or absolute if required)
TOOL_PATHS = {
    "sqlmap": os.path.join(BASE_DIR, "Library", "sqlmap"),
    "nuclei": os.path.join(BASE_DIR, "Library", "nuclei"),
    "hydra": os.path.join(BASE_DIR, "Library", "hydra"),
    "commix": os.path.join(BASE_DIR, "Library", "commix"),
    "ffuf": os.path.join(BASE_DIR, "Library", "ffuf"),
    "dalfox": os.path.join(BASE_DIR, "Library", "dalfox"),
    "xsstrike": os.path.join(BASE_DIR, "Library", "xsstrike"),
    "jwt_tool": os.path.join(BASE_DIR, "Library", "jwt_tool"),
    "corsy": os.path.join(BASE_DIR, "Library", "corsy"),
    "ssrfmap": os.path.join(BASE_DIR, "Library", "ssrfmap"),
    "oralyzer": os.path.join(BASE_DIR, "Library", "oralyzer"),
    "cmsmap": os.path.join(BASE_DIR, "Library", "cmsmap"),
    "gospider": os.path.join(BASE_DIR, "Library", "gospider"),
    "subfinder": os.path.join(BASE_DIR, "Library", "subfinder"),
    "waybackurls": os.path.join(BASE_DIR, "Library", "waybackurls"),
    "paramminer": os.path.join(BASE_DIR, "Library", "paramminer"),
    "searchsploit": os.path.join(BASE_DIR, "Library", "exploitdb"),
    "ncrack": os.path.join(BASE_DIR, "Library", "ncrack"),
    "medusa": os.path.join(BASE_DIR, "Library", "medusa"),
    # Add other tools as needed
}

# Local module paths (relative to BASE_DIR)
MODULE_PATHS = {
    "ai_logic": os.path.join(BASE_DIR, "ai_logic"),
    "bot": os.path.join(BASE_DIR, "bot"),
    "brute": os.path.join(BASE_DIR, "brute"),
    "crawler": os.path.join(BASE_DIR, "crawler"),
    "dork_gen": os.path.join(BASE_DIR, "dork_gen"),
    "dump": os.path.join(BASE_DIR, "dump"),
    "exploit": os.path.join(BASE_DIR, "exploit"),
    "notifier": os.path.join(BASE_DIR, "notifier"),
    "plugin": os.path.join(BASE_DIR, "plugin"),
    "proxy_engine": os.path.join(BASE_DIR, "proxy_engine"),
    "recon": os.path.join(BASE_DIR, "recon"),
    "shell": os.path.join(BASE_DIR, "shell"),
    "utils": os.path.join(BASE_DIR, "utils"),
}

# General bot settings
MAX_CONCURRENT_TASKS = 10
PROXY_ROTATION_INTERVAL = 300  # seconds
ZIP_OUTPUT_FOLDER = os.path.join(BASE_DIR, "loot_zips")
LOG_FILE = os.path.join(BASE_DIR, "bot_logs", "pentest_bot.log")
LOG_LEVEL = "DEBUG"

# Ensure output folders exist
os.makedirs(ZIP_OUTPUT_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Notification settings
NOTIFY_ON_HIT = True
NOTIFY_ON_SHELL = True
NOTIFY_ON_DUMP = True

# Optional: folders for wordlists/payloads
WORDLISTS_PATH = os.path.join(BASE_DIR, "utils", "wordlists")  # Adjust to actual wordlists folder
PAYLOADS_PATH = os.path.join(BASE_DIR, "utils", "payloads")    # Adjust to actual payloads folder

# Optional: API keys/config for external services (uncomment and use if required)
# SHODAN_API_KEY = "your_shodan_api_key_here"
# CENSYS_API_ID = ""
# CENSYS_API_SECRET = ""
