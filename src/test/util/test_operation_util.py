import unittest
from src.main.util.operation_util import OperationUtil
from src.main.dto.operation_dto import OperationDto
from src.main.enum.operation_type_enum import OperationTypeEnum

class TestOperationUtil(unittest.TestCase):
    def test_format_operations_file_valid(self):
        #Given
        lines = [
            '[{"operation":"buy", "unit-cost":10.00, "quantity": 10000}, {"operation":"sell", "unit-cost":20.00, "quantity": 5000}]',
            '[{"operation":"buy", "unit-cost":20.00, "quantity": 10000}]'
        ]

        #When
        result = OperationUtil.format_operations_file(lines)

        #Then
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0][0], OperationDto)
        self.assertEqual(result[0][0].operation, OperationTypeEnum.BUY)
        self.assertEqual(result[0][1].operation, OperationTypeEnum.SELL)
        self.assertEqual(result[1][0].unit_cost, 20.00)
        self.assertEqual(result[1][0].quantity, 10000)

    def test_format_operations_file_empty_lines(self):
        #Given
        lines = [
            '',
            '   ',
            '[{"operation":"buy", "unit-cost":10.00, "quantity": 10000}]'
        ]

        #When
        result = OperationUtil.format_operations_file(lines)

        #Then
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0].operation, OperationTypeEnum.BUY)

    def test_format_operations_file_invalid_json(self):
        #Given
        lines = [
            '[{"operation":"buy", "unit-cost":10.00, "quantity": 10000}',
        ]

        #Then
        with self.assertRaises(Exception):
            OperationUtil.format_operations_file(lines)

if __name__ == "__main__":
    unittest.main()
