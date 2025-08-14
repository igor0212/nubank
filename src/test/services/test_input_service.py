import unittest
from src.main.services.input_service import InputService
from src.main.services.operation_service import OperationService
from src.main.utils.operation_util import OperationUtil
from src.main.exceptions.exception import OperationProcessingError


class TestInputService(unittest.TestCase):
    def setUp(self):
        self.input_service = InputService(
            operation_service=OperationService(),
            operation_util=OperationUtil
        )

    def test_process_input_valid(self):
        # Given
        lines = [
            '[{"operation":"buy", "unit-cost":10.00, "quantity": 100}, {"operation":"sell", "unit-cost":15.00, "quantity": 50}]',
            '[{"operation":"buy", "unit-cost":20.00, "quantity": 100}]'
        ]

        # When
        result = self.input_service.process_input(lines)

        # Then
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(line, list) for line in result))
        self.assertEqual(len(result), 2)

    def test_process_input_empty_lines(self):
        # Given
        lines = [
            '',
            '   ',
            '[{"operation":"buy", "unit-cost":10.00, "quantity": 100}]'
        ]
        # When
        result = self.input_service.process_input(lines)

        # Thens
        self.assertEqual(len(result), 1)

    def test_process_input_invalid_json(self):
        # Given
        lines = [
            '[{"operation":"buy", "unit-cost":10.00, "quantity": 100}'
        ]

        # Then
        with self.assertRaises(OperationProcessingError):
            self.input_service.process_input(lines)

    def test_process_input_missing_fields(self):
        # Given
        lines = [
            '[{"operation":"buy", "quantity": 100}]'
        ]

        # Thens
        with self.assertRaises(OperationProcessingError):
            self.input_service.process_input(lines)

    def test_process_input_invalid_operation_type(self):
        # Given
        lines = [
            '[{"operation":"invalid", "unit-cost":10.00, "quantity": 100}]'
        ]

        # Then
        with self.assertRaises(OperationProcessingError):
            self.input_service.process_input(lines)


if __name__ == "__main__":
    unittest.main()
