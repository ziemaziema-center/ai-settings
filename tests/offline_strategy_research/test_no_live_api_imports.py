import unittest
from _test_utils import harness_python_files, read_text


class TestNoLiveApiImports(unittest.TestCase):
    def test_no_live_api_imports(self):
        forbidden_tokens = [
            "import requests",
            "from requests",
            "import httpx",
            "from httpx",
            "import aiohttp",
            "from aiohttp",
            "import websocket",
            "from websocket",
            "import socket",
            "from socket",
            "http.client",
            "urllib.request",
            "urllib3",
        ]
        for path in harness_python_files():
            text = read_text(path)
            for token in forbidden_tokens:
                self.assertNotIn(token, text, f"Forbidden import in {path.name}: {token}")


if __name__ == "__main__":
    unittest.main()
