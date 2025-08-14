import unittest
import subprocess
import sys
import os


class TestMainIntegration(unittest.TestCase):
    def test_main_with_valid_input(self):
        # Given
        sample_input = (
            '[{"operation":"buy", "unit-cost":10.00, "quantity": 100}, {"operation":"sell", "unit-cost":15.00, "quantity": 50},{"operation":"sell", "unit-cost":15.00, "quantity": 50}]\n'
            '[{"operation":"buy", "unit-cost":10.00, "quantity": 10000},{"operation":"sell", "unit-cost":20.00, "quantity": 5000},{"operation":"sell", "unit-cost":5.00, "quantity": 5000}]\n'
        )

        expected = "[[{'tax': 0.0}, {'tax': 0.0}, {'tax': 0.0}], [{'tax': 0.0}, {'tax': 10000.0}, {'tax': 0.0}]]"

        # Path to main.py
        main_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "main", "main.py"
        )

        # Run main.py as a subprocess, feeding sample_input to stdin
        # Set PYTHONPATH to the project root so 'src' is importable
        env = os.environ.copy()
        project_root = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.dirname(__file__))))
        env["PYTHONPATH"] = project_root + \
            os.pathsep + env.get("PYTHONPATH", "")

        # When
        result = subprocess.run(
            [sys.executable, main_path],
            input=sample_input.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env
        )

        actual = result.stdout.decode().strip()

        # Then
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
