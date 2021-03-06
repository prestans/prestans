import unittest

from prestans.devel.exception import Base


class ExceptionBaseTest(unittest.TestCase):

    def test_message(self):
        message_custom = Base("message")
        self.assertEqual(message_custom.message, "message")
        self.assertEqual(str(message_custom), "message")

    def test_error_code(self):
        error_code_default = Base("message")
        self.assertEqual(error_code_default.error_code, 2)

        error_code_custom = Base("message", error_code=3)
        self.assertEqual(error_code_custom.error_code, 3)
