import unittest
from src.main.service.OperationService import OperationService
from src.main.dto.OperationDto import OperationDto

class OperationServiceTest(unittest.TestCase):
    def test_process_operations_returns_tax_results(self):
        # Given
        actual = [
            [
                OperationDto("buy", 10.00, 10000),
                OperationDto("sell", 20.00, 5000)
            ],
            [
                OperationDto("buy", 20.00, 10000),
                OperationDto("sell", 10.00, 5000)
            ]
        ]

        # When
        expected = OperationService.processOperations(actual)        

        # Then
        self.assertEqual(len(actual), len(expected))
        for i in range(len(actual)):
            self.assertEqual(len(actual[i]), len(expected[i]))

if __name__ == "__main__":
    unittest.main()
