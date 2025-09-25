import os
import logging

logger = logging.getLogger(__name__)

def load_wordlist(wordlist_path):
    """
    Load wordlist file lines into list.
    Returns list of strings or empty list if file not found/error.
    """
    if not os.path.exists(wordlist_path):
        logger.warning(f"Wordlist not found: {wordlist_path}")
        return []

    try:
        with open(wordlist_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines
    except Exception as e:
        logger.error(f"Error reading wordlist {wordlist_path}: {e}")
        return []
