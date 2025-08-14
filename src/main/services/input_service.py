from typing import List
from src.main.services.operation_service import OperationService
from src.main.utils.operation_util import OperationUtil
from src.main.dto.operation_dto import OperationDto


class InputService:
    """
    Service to process input lines and delegate to operation processing.
    Allows dependency injection for easier testing and flexibility.
    """

    def __init__(self, operation_service=None, operation_util=None):
        """
        Args:
            operation_service: Instance of OperationService. Defaults to OperationService().
            operation_util: Utility class for formatting operations. Defaults to OperationUtil.
        """
        self.operation_service = operation_service or OperationService()
        self.operation_util = operation_util or OperationUtil

    def process_input(self, lines: List[str]) -> list[list[dict]]:
        """
        Process input lines, format them as operations, and calculate taxes.

        Args:
            lines (List[str]): Lines of input, each a JSON array of operations.

        Returns:
            list: List of lists of OperationTaxDto as dicts.
        """
        operations_list: list[list[OperationDto]
                              ] = self.operation_util.format_operations_file(lines)
        return self.operation_service.process_operations(operations_list)
