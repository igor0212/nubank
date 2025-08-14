import unittest
from src.main.service.operation_service import OperationService
from src.main.enum.operation_type_enum import OperationTypeEnum
from src.main.dto.operation_dto import OperationDto

class TestOperationService(unittest.TestCase):
    def check_process_operations(self, expected, expected_lengths):
        #When
        actual = OperationService.process_operations(expected)        

        #Then
        self.assertEqual(len(expected), len(actual))
        for i in range(len(expected)):
            self.assertEqual(len(expected[i]), len(actual[i]))
            if expected_lengths:
                self.assertEqual(len(actual[i]), expected_lengths[i])

    def test_process_operations_returns_tax_results(self):
        #Given
        actual = [
            [
                OperationDto(OperationTypeEnum.BUY, 10.00, 10000),
                OperationDto(OperationTypeEnum.SELL, 20.00, 5000)
            ],
            [
                OperationDto(OperationTypeEnum.BUY, 20.00, 10000),
                OperationDto(OperationTypeEnum.SELL, 10.00, 5000)
            ]
        ]

        expected_lengths = [2, 2]

        self.check_process_operations(actual, expected_lengths)

    def test_process_operations_returns_tax_results_when_single_operation_each_list(self):
        #Given
        actual = [
            [OperationDto(OperationTypeEnum.BUY, 5.00, 1000)],
            [OperationDto(OperationTypeEnum.SELL, 25.00, 2000)]
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
