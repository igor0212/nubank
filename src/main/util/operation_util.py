"""
Operation util for application. It provides utility functions for processing operations.
"""

import json
from src.main.dto.operation_dto import OperationDto


class OperationUtil:
    """
    Utility class for formatting and processing operation input data.
    """

    @staticmethod
    def format_operations_file(lines) -> list[list[OperationDto]]:
        """
        Format each received line (each must be a JSON list of operations).

        Args:
            lines (list[str]): Lines of input, each a JSON array of operations.

        Returns:
            list: List of lists of OperationDto objects.
        """
        results = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                operations_list = json.loads(line)
                results.append([OperationDto.from_dict(op)
                               for op in operations_list])
            except Exception:
                raise ValueError(f"Invalid input: {line}")

        return results
