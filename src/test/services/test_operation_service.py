import unittest
from src.main.services.operation_service import OperationService
from src.main.dto.operation_dto import OperationDto, OperationTypeEnum


class TestOperationService(unittest.TestCase):
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
        expected = OperationService.process_operations(actual)
        self.assertEqual(len(actual), len(expected))
        for i in range(len(actual)):
            self.assertEqual(len(actual[i]), len(expected[i]))

    def test_process_operations_empty(self):
        actual = []
        expected = OperationService.process_operations(actual)
        self.assertEqual(expected, [])

    def test_process_operations_invalid_input(self):
        # Should raise if input is not a list of lists of OperationDto
        with self.assertRaises(Exception):
            OperationService.process_operations([{"operation": "buy"}])


if __name__ == "__main__":
    unittest.main()
