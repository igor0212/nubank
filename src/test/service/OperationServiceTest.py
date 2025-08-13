import unittest
from src.main.service.OperationService import OperationService
from src.main.dto.OperationDto import OperationDto

class OperationServiceTest(unittest.TestCase):
    def check_process_operations(self, actual, expected_lengths):
        #When
        expected = OperationService.processOperations(actual)        

        #Then
        self.assertEqual(len(actual), len(expected))
        for i in range(len(actual)):
            self.assertEqual(len(actual[i]), len(expected[i]))
            if expected_lengths:
                self.assertEqual(len(expected[i]), expected_lengths[i])

    def test_process_operations_returns_tax_results(self):
        #Given
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
        
        self.check_process_operations(actual, [2, 2])

    def test_process_operations_returns_tax_results_when_single_operation_each_list(self):
        #Given
        actual = [
            [OperationDto("buy", 5.00, 1000)],
            [OperationDto("sell", 25.00, 2000)]
        ]
        self.check_process_operations(actual, [1, 1])

    def test_process_operations_returns_tax_results_when_empty_operation(self):
        #Given
        actual = []
        self.check_process_operations(actual, [])

if __name__ == "__main__":
    unittest.main()
