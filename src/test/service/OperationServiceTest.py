import unittest
from src.main.service.OperationService import OperationService
from src.main.enum.OperationType import OperationType
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
                OperationDto(OperationType.BUY, 10.00, 10000),
                OperationDto(OperationType.SELL, 20.00, 5000)
            ],
            [
                OperationDto(OperationType.BUY, 20.00, 10000),
                OperationDto(OperationType.SELL, 10.00, 5000)
            ]
        ]

        expected_lengths = [2, 2]

        self.check_process_operations(actual, expected_lengths)

    def test_process_operations_returns_tax_results_when_single_operation_each_list(self):
        #Given
        actual = [
            [OperationDto(OperationType.BUY, 5.00, 1000)],
            [OperationDto(OperationType.SELL, 25.00, 2000)]
        ]

        expected_lengths = [1, 1]

        self.check_process_operations(actual, expected_lengths)

    def test_process_operations_returns_tax_results_when_empty_operation(self):
        #Given
        actual = []
        expected_lengths = []

        self.check_process_operations(actual, expected_lengths)

if __name__ == "__main__":
    unittest.main()
    unittest.main()
