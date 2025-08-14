"""
Main application entry point.
"""
import sys
from src.main.services.operation_service import OperationService
from src.main.utils.operation_util import OperationUtil
from src.main.exceptions.exception import OperationProcessingError


def main() -> None:
    """
    Reads lists (one per line) of stock market operations in JSON format via stdin,
    processes them, and outputs the tax results.

    Example input:
    [{"operation":"buy", "unit-cost":10.00, "quantity": 10000},{"operation":"sell", "unit-cost":20.00, "quantity": 5000}]
    [{"operation":"buy", "unit-cost":20.00, "quantity": 10000}, {"operation":"sell", "unit-cost":10.00, "quantity": 5000}]
    """
    lines = sys.stdin.readlines()
    try:
        operations_list = OperationUtil.format_operations_file(lines)
        results = OperationService.process_operations(operations_list)
        sys.stdout.write(str(results))
    except Exception as e:
        raise OperationProcessingError(str(e))


if __name__ == "__main__":
    main()
