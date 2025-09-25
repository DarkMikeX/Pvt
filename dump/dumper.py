import os
import re
import logging

logger = logging.getLogger(__name__)

class Dumper:
    def __init__(self, output_dir="dumps"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_dump(self, dump_name, data):
        """
        Save dump data to a file under output_dir with dump_name
        """
        file_path = os.path.join(self.output_dir, dump_name)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(data)
            logger.info(f"Saved dumped data to: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Failed to save dump: {e}")
            return None

    def parse_and_save(self, raw_output):
        """
        Parse raw tool output to extract interesting dumps such as credentials, tokens, etc.
        This is a simplistic implementation; enhance per tool output format.

        Returns list of saved file paths.
        """
        saved_files = []

        # Example regexes for .env keys, tokens, DB creds
        env_match = re.findall(r'(?i)([\w_]+)=([^\s]+)', raw_output)
        if env_match:
            env_content = "\n".join(f"{k}={v}" for k, v in env_match)
            path = self.save_dump("env_vars.txt", env_content)
            if path:
                saved_files.append(path)

        # Dummy example for credit card or token extraction (expand regexes)
        creds_match = re.findall(r'(password|user|token)[^\s=]*=[^\s]+', raw_output, re.IGNORECASE)
        if creds_match:
            creds_content = "\n".join(creds_match)
            path = self.save_dump("credentials.txt", creds_content)
            if path:
                saved_files.append(path)

        # Add custom parsing for SQL dumps, config leaks, etc.

        if not saved_files:
            logger.info("No dump patterns matched in output")

        return saved_files
