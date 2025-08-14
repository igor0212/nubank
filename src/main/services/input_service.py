from typing import List
from src.main.services.operation_service import OperationService
from src.main.utils.operation_util import OperationUtil
from src.main.dto.operation_dto import OperationDto


class InputService:
    """
    Service to process input lines and delegate to operation processing.
    """
    @staticmethod
    def process_input(lines: List[str]) -> list[list[dict]]:
        """
        Process input lines, format them as operations, and calculate taxes.

        Args:
            lines (List[str]): Lines of input, each a JSON array of operations.

        Returns:
            list: List of lists of OperationTaxDto as dicts.
        """
        operations_list: list[list[OperationDto]
                              ] = OperationUtil.format_operations_file(lines)
        return OperationService.process_operations(operations_list)
