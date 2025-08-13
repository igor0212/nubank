"""
Main application entry point.
"""
import logging
import sys
import json 
from util.Logger import log

def process_operations_file(lines):
    """
    Processes each received line (each must be a JSON list of operations).
    Returns a list of lists of operations.
    """
    results = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            operations_list = json.loads(line)
            results.append(operations_list)
        except Exception:
            message = f"Invalid input: {line}"
            log(logging.ERROR, message)
            raise Exception(message)
    return results


def main() -> None:
    """
    Receives lists (one per line) of stock market operations in JSON format via stdin.
    Example input:
    [{"operation":"buy", "unit-cost":10.00, "quantity": 10000},{"operation":"sell", "unit-cost":20.00, "quantity": 5000}]
    [{"operation":"buy", "unit-cost":20.00, "quantity": 10000}, {"operation":"sell", "unit-cost":10.00, "quantity": 5000}]
    """
    lines = sys.stdin.readlines()
    try:
        results = process_operations_file(lines)
        print(json.dumps({"received": results}))
    except Exception:        
        sys.exit(1)
    return

if __name__ == "__main__":        
    main()
