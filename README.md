# How to run the main?

To call the main method in the terminal, run the command below from the project root:

    python -m src.main.main

Then, paste the JSON lists (one per line) and press Ctrl+D (Linux/Mac) or Ctrl+Z followed by Enter (Windows) to finish the input.

Example:

[{"operation":"buy", "unit-cost":10.00, "quantity": 10000},{"operation":"sell", "unit-cost":20.00, "quantity": 5000}]
[{"operation":"buy", "unit-cost":20.00, "quantity": 10000},{"operation":"sell", "unit-cost":10.00, "quantity": 5000}]


# How to run unit tests?

Run from the project root:

To run all tests:

    python -m unittest discover -s src/test -p "*.py"

To run a specific test:

    python -m src.test.service.test_operation_service

