"""
Operation service for application. It handles the processing of stock market operations and 
tax calculations.
"""

from src.main.dto.operation_dto import OperationDto
from src.main.services.tax_service import TaxService
from src.main.exceptions.exception import OperationProcessingError


class OperationService:
    """
    Service for processing lists of operations and calculating taxes.
    """

    @staticmethod
    def process_operations(operations: list[list[OperationDto]]) -> list[list[dict]]:
        """
        Gets a list of lists of OperationDto and returns a list of tax results for each operation.

        Args:
            operations (list[list[OperationDto]]): List of lists of OperationDto.

        Returns:
            list: List of lists of OperationTaxDto as dicts.
        """
        try:
            tax_results = []
            for operation_dto_list in operations:
                operation_taxes = TaxService.calculate_taxes(
                    operation_dto_list)
                tax_results.append(operation_taxes)
            return tax_results
        except Exception as e:
            raise OperationProcessingError(
                f"Error processing operation: {str(e)}")
