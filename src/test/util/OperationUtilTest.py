import unittest
from src.main.util.OperationUtil import OperationUtil
from src.main.dto.OperationDto import OperationDto, OperationType

class OperationUtilTest(unittest.TestCase):
    def test_format_operations_file_valid(self):
        lines = [
            '[{"operation":"buy", "unit-cost":10.00, "quantity": 10000}, {"operation":"sell", "unit-cost":20.00, "quantity": 5000}]',
            '[{"operation":"buy", "unit-cost":20.00, "quantity": 10000}]'
        ]
        result = OperationUtil.formatOperationsFile(lines)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0][0], OperationDto)
        self.assertEqual(result[0][0].operation, OperationType.BUY)
        self.assertEqual(result[0][1].operation, OperationType.SELL)
        self.assertEqual(result[1][0].unit_cost, 20.00)
        self.assertEqual(result[1][0].quantity, 10000)

    def test_format_operations_file_empty_lines(self):
        lines = [
            '',
            '   ',
            '[{"operation":"buy", "unit-cost":10.00, "quantity": 10000}]'
        ]
        result = OperationUtil.formatOperationsFile(lines)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0].operation, OperationType.BUY)

    def test_format_operations_file_invalid_json(self):
        lines = [
            '[{"operation":"buy", "unit-cost":10.00, "quantity": 10000}',
        ]
        with self.assertRaises(Exception):
            OperationUtil.formatOperationsFile(lines)

if __name__ == "__main__":
    unittest.main()
