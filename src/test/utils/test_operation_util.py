import unittest
from src.main.exceptions.exception import OperationProcessingError
from src.main.utils.operation_util import OperationUtil
from src.main.dto.operation_dto import OperationDto, OperationTypeEnum


class TestOperationUtil(unittest.TestCase):
    def test_format_operations_file_valid(self):
        # Given
        lines = [
            '[{"operation":"buy", "unit-cost":10.00, "quantity": 10000}, {"operation":"sell", "unit-cost":20.00, "quantity": 5000}]',
            '[{"operation":"buy", "unit-cost":20.00, "quantity": 10000}]'
        ]

        # When
        actual = OperationUtil.format_operations_file(lines)

        # Then
        self.assertEqual(len(actual), 2)
        self.assertIsInstance(actual[0][0], OperationDto)
        self.assertEqual(actual[0][0].operation, OperationTypeEnum.BUY)
        self.assertEqual(actual[0][1].operation, OperationTypeEnum.SELL)
        self.assertEqual(actual[1][0].unit_cost, 20.00)
        self.assertEqual(actual[1][0].quantity, 10000)

    def test_format_operations_file_empty_lines(self):
        # Given
        lines = [
            '',
            '   ',
            '[{"operation":"buy", "unit-cost":10.00, "quantity": 10000}]'
        ]

        # When
        actual = OperationUtil.format_operations_file(lines)

        # Then
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0][0].operation, OperationTypeEnum.BUY)

    def test_format_operations_file_invalid_json(self):
        # Given
        lines = [
            '[{"operation":"buy", "unit-cost":10.00, "quantity": 10000}',
        ]

        # Then
        with self.assertRaises(OperationProcessingError):
            OperationUtil.format_operations_file(lines)

    def test_format_operations_file_invalid_operation_type(self):
        # Given
        lines = [
            '[{"operation":"invalid", "unit-cost":10.00, "quantity": 10000}]'
        ]

        # Then
        with self.assertRaises(OperationProcessingError):
            OperationUtil.format_operations_file(lines)


if __name__ == "__main__":
    unittest.main()
