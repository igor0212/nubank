"""
Main application entry point.
"""
import sys
import json
from main.service.OperationService import OperationService
from util.OperationUtil import OperationUtil

def main() -> None:
    """
    Receives lists (one per line) of stock market operations in JSON format via stdin.
    Example input:
    [{"operation":"buy", "unit-cost":10.00, "quantity": 10000},{"operation":"sell", "unit-cost":20.00, "quantity": 5000}]
    [{"operation":"buy", "unit-cost":20.00, "quantity": 10000}, {"operation":"sell", "unit-cost":10.00, "quantity": 5000}]
    """
    lines = sys.stdin.readlines()
    try:
        operations = OperationUtil.formatOperationsFile(lines)
        results = OperationService.processOperations(operations)
        print(json.dumps({"results": results}))
    except Exception as e:
        raise Exception(str(e))        
    return

if __name__ == "__main__":        
    main()
