import unittest
from service.main_service import MainService

class TestMainService(unittest.TestCase):
    def test_process(self):
        service = MainService()
        result = service.process("test")
        self.assertEqual(result, "test")

if __name__ == "__main__":
    unittest.main()
