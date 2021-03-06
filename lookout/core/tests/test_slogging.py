import io
import json
import logging
import sys
import tempfile
import unittest

from lookout.core import slogging


class SloggingTests(unittest.TestCase):
    def test_structured_logging(self):
        logging.basicConfig()
        handler_backup = logging.getLogger().handlers[0]
        slogging.setup("INFO", True)
        backup = sys.stdout
        sys.stdout = buffer = io.StringIO()
        try:
            logging.getLogger("test").info("hello, world!")
        finally:
            sys.stdout = backup
        logging.getLogger().handlers[0] = handler_backup
        obj = json.loads(buffer.getvalue())
        self.assertEqual(obj["level"], "info")
        self.assertEqual(obj["msg"], "hello, world!")
        self.assertEqual(obj["source"], "test_slogging.py:19")
        self.assertEqual(len(obj["thread"]), 4)
        self.assertIn("time", obj)

    def test_config(self):
        slogging.setup("INFO", True, "XXX.yml")
        with tempfile.NamedTemporaryFile() as f:
            f.write(b"FormatAnalyzer: INFO\nRules: INFO\nTrainableRules: INFO\n")
            f.flush()
            slogging.setup("INFO", True, f.name)


if __name__ == "__main__":
    unittest.main()
