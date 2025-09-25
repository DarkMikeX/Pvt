import subprocess
import shlex
import os
import logging

logger = logging.getLogger(__name__)

class ReconCrawler:
    def __init__(self, tool_paths, output_dir="recon_output"):
        self.subfinder_path = tool_paths.get("subfinder")
        self.gospider_path = tool_paths.get("gospider")
        self.waybackurls_path = tool_paths.get("waybackurls")
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def run_subfinder(self, domain):
        if not self.subfinder_path:
            logger.error("Subfinder path not set.")
            return False, "Subfinder path missing"

        output_file = os.path.join(self.output_dir, f"{domain}_subdomains.txt")
        cmd = f"{self.subfinder_path} -d {domain} -o {output_file} -silent"

        logger.info(f"Running subfinder: {cmd}")
        return self._run_command(cmd), output_file

    def run_gospider(self, domain):
        if not self.gospider_path:
            logger.error("Gospider path not set.")
            return False, "Gospider path missing"

        output_format = "json"  # or html/text
        output_file = os.path.join(self.output_dir, f"{domain}_gospider.{output_format}")
        cmd = (f"{self.gospider_path} -s https://{domain} "
               f"-o {output_file} -q -c 10 -d 3 --other-source")

        logger.info(f"Running gospider: {cmd}")
        return self._run_command(cmd), output_file

    def run_waybackurls(self, domain):
        if not self.waybackurls_path:
            logger.error("Waybackurls path not set.")
            return False, "Waybackurls path missing"

        output_file = os.path.join(self.output_dir, f"{domain}_waybackurls.txt")
        cmd = f"echo {domain} | {self.waybackurls_path} > {output_file}"

        logger.info(f"Running waybackurls: {cmd}")
        try:
            process = subprocess.run(cmd, shell=True, timeout=300)
            if process.returncode == 0:
                return True, output_file
            else:
                return False, "Waybackurls failed"
        except Exception as e:
            logger.error(f"Waybackurls exception: {e}")
            return False, str(e)

    def _run_command(self, cmd):
        try:
            process = subprocess.run(
                shlex.split(cmd),
                capture_output=True,
                text=True,
                timeout=600,
            )
            if process.returncode == 0:
                logger.info("Command finished successfully.")
                return True
            else:
                logger.error(f"Command error: {process.stderr}")
                return False
        except Exception as e:
            logger.error(f"Exception running command: {e}")
            return False
