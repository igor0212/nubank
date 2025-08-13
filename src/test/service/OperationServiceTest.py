import unittest
from src.main.service.OperationService import OperationService

class OperationServiceTest(unittest.TestCase):
    def test_should_call_operation_service_when_process_operation(self):
        # Given
        actual = [[{"operation":"buy", "unit-cost":10.00, "quantity": 10000},{"operation":"sell", "unit-cost":20.00, "quantity": 5000}],
                  [{"operation":"buy", "unit-cost":20.00, "quantity": 10000}, {"operation":"sell", "unit-cost":10.00, "quantity": 5000}]]

        # When
        expected = OperationService.processOperations(actual)

        # Then
        self.assertEqual(len(actual), len(expected))

if __name__ == "__main__":
    unittest.main()
