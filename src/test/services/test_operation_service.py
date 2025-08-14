import unittest
from src.main.services.operation_service import OperationService
from src.main.services.tax_service import TaxService
from src.main.dto.operation_dto import OperationDto, OperationTypeEnum


class TestOperationService(unittest.TestCase):
    def setUp(self):
        self.operation_service = OperationService(tax_service=TaxService())

    def test_process_operations_returns_tax_results(self):
        # Given
        operations = [
            [
                OperationDto(OperationTypeEnum.BUY, 10.00, 10000),
                OperationDto(OperationTypeEnum.SELL, 20.00, 5000)
            ],
            [
                OperationDto(OperationTypeEnum.BUY, 20.00, 10000),
                OperationDto(OperationTypeEnum.SELL, 10.00, 5000)
            ]
        ]

        # When
        actual = self.operation_service.process_operations(operations)

        # Then
        self.assertEqual(len(operations), len(actual))
        for i in range(len(operations)):
            self.assertEqual(len(operations[i]), len(actual[i]))

    def test_process_operations_empty(self):
        # Given
        expected = []

        # When
        actual = self.operation_service.process_operations(expected)

        # Then
        self.assertEqual(actual, expected)

    def test_process_operations_invalid_input(self):
        # Given
        operations = [{"operation": "buy"}]

        # Then
        with self.assertRaises(Exception):
            self.operation_service.process_operations(operations)


if __name__ == "__main__":
    unittest.main()
