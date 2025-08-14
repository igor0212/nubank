import unittest
from src.main.services.operation_service import OperationService
from src.main.services.tax_service import TaxService
from src.main.dto.operation_dto import OperationDto, OperationTypeEnum


class TestOperationService(unittest.TestCase):
    def setUp(self):
        # Inject dependency for testability
        self.operation_service = OperationService(tax_service=TaxService)

    def test_process_operations_returns_tax_results(self):
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
        expected = self.operation_service.process_operations(actual)
        self.assertEqual(len(actual), len(expected))
        for i in range(len(actual)):
            self.assertEqual(len(actual[i]), len(expected[i]))

    def test_process_operations_empty(self):
        actual = []
        expected = self.operation_service.process_operations(actual)
        self.assertEqual(expected, [])

    def test_process_operations_invalid_input(self):
        # Should raise if input is not a list of lists of OperationDto
        with self.assertRaises(Exception):
            self.operation_service.process_operations([{"operation": "buy"}])


if __name__ == "__main__":
    unittest.main()
