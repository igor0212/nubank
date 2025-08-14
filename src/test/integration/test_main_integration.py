import unittest
import subprocess
import sys
import os

class TestMainIntegration(unittest.TestCase):
    def test_main_with_valid_input(self):
        # Sample input: two lines, each a list of operations
        sample_input = (
            '[{"operation":"buy", "unit-cost":10.00, "quantity": 100}, {"operation":"sell", "unit-cost":15.00, "quantity": 50}]\n'
            '[{"operation":"buy", "unit-cost":20.00, "quantity": 100}, {"operation":"sell", "unit-cost":10.00, "quantity": 50}]\n'
        )

        # Path to main.py
        main_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "main", "main.py"
        )

        # Run main.py as a subprocess, feeding sample_input to stdin
        result = subprocess.run(
            [sys.executable, main_path],
            input=sample_input.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        output = result.stdout.decode().strip()
        error_output = result.stderr.decode().strip()
        if result.returncode != 0:
            print("STDERR:", error_output)
        # Check if output contains expected keys (e.g., "tax" or a list structure)
        self.assertTrue("tax" in output or "[" in output)

if __name__ == "__main__":
    unittest.main()
