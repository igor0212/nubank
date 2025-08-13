"""
Operation util for application.
"""

import json
from dto.OperationDto import OperationDto

class OperationUtil:
    """Util for operations."""
    
    @staticmethod
    def formatOperationsFile(lines):
        """
        Format each received line (each must be a JSON list of operations).        

        Returns:
            list: List of OperationDto objects.
        """
        results = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                operations_list = json.loads(line)
                results.append([OperationDto.from_dict(op) for op in operations_list])                
            except Exception:
                raise Exception(f"Invalid input: {line}")
            
        return results
    