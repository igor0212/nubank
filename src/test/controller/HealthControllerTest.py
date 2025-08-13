import unittest
from controller.HealthControllerTest import MainController
from service.MainServiceTest import MainService

class TestControllerServiceIntegration(unittest.TestCase):
    def test_handle_request(self):
        service = MainService()
        controller = MainController(service)
        result = controller.handle_request("integration")
        self.assertEqual(result, "integration")

if __name__ == "__main__":
    unittest.main()
