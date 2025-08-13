"""
Operation util for application.
"""

import json

class OperationUtil:
    """Util for operations."""
    
    def formatOperationsFile(lines):
        """
        Format each received line (each must be a JSON list of operations).
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
                raise Exception(f"Invalid input: {line}")
            
        return results
    