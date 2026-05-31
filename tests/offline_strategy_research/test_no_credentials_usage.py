import unittest
from _test_utils import harness_python_files, read_text


class TestNoCredentialsUsage(unittest.TestCase):
    def test_no_credentials_usage(self):
        forbidden_tokens = [
            "os.environ",
            "getenv(",
            "dotenv",
            "UPBIT_ACCESS_KEY",
            "UPBIT_SECRET_KEY",
            "CredentialManager",
        ]
        for path in harness_python_files():
            text = read_text(path)
            for token in forbidden_tokens:
                self.assertNotIn(token, text, f"Credential token in {path.name}: {token}")


if __name__ == "__main__":
    unittest.main()
