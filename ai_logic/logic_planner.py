import logging

logger = logging.getLogger(__name__)

class LogicPlanner:
    def __init__(self):
        """
        Initializes the planner state including recon status, found vulnerabilities,
        obtained shells, and collected dumps.
        """
        self.state = {
            "recon_done": False,
            "vulnerabilities_found": set(),
            "shells_obtained": set(),
            "dumps_collected": set()
        }

    def update_state(self, key, value):
        """
        Update internal state keys with new values. For sets, values are added.
        """
        if key not in self.state:
            logger.warning(f"Unknown state key: {key}")
            return

        if isinstance(self.state[key], set):
            if isinstance(value, (list, set)):
                self.state[key].update(value)
            else:
                self.state[key].add(value)
        else:
            self.state[key] = value

        logger.info(f"State updated: {key} = {self.state[key]}")

    def clear_state(self, key):
        """
        Clear values for a key if applicable, e.g. empty a set or reset flags.
        """
        if key not in self.state:
            logger.warning(f"Unknown state key: {key}")
            return

        if isinstance(self.state[key], set):
            self.state[key].clear()
        elif isinstance(self.state[key], bool):
            self.state[key] = False
        else:
            self.state[key] = None

        logger.info(f"State cleared: {key}")

    def suggest_next_actions(self):
        """
        Analyze the current state and suggest next workflow steps for pentesting automation.
        Returns a list of string action identifiers.
        """

        # If recon hasn't been done, prioritize it
        if not self.state["recon_done"]:
            logger.info("Suggesting recon phase.")
            return ["run_recon"]

        # Prioritize exploitation based on known vulnerabilities
        vulns = self.state["vulnerabilities_found"]
        suggestions = []

        if "sql_injection" in vulns:
            suggestions.append("run_sql_dump")
            suggestions.append("upload_shell")

        if "lfi" in vulns:
            suggestions.append("test_rce")
            suggestions.append("upload_shell")

        if "rce" in vulns:
            suggestions.append("upload_shell")

        if "xss" in vulns:
            suggestions.append("xss_exploit")

        if "ssrf" in vulns:
            suggestions.append("ssrf_exploit")

        if "open_redirect" in vulns:
            suggestions.append("open_redirect_test")

        # If no vulns known and no shells, fallback to recon or crawling deeper
        if not suggestions and not self.state["shells_obtained"]:
            logger.info("No known vulns and no shells, fallback to crawling.")
            return ["recursive_crawl"]

        # If shells are obtained, focus on dumping and maintaining shells
        if self.state["shells_obtained"]:
            if not self.state["dumps_collected"]:
                suggestions.append("run_dump")
            else:
                suggestions.append("maintain_shell")
                suggestions.append("enumerate")

        # If no suggestions, fallback to recon or idle
        if not suggestions:
            logger.info("No specific suggestions, fallback to recon idle.")
            return ["run_recon"]

        logger.info(f"Suggested next actions: {suggestions}")
        return suggestions

