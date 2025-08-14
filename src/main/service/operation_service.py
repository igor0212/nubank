"""
Operation service for application.
"""

from src.main.dto.operation_dto import OperationDto
from src.main.service.tax_service import TaxService

class OperationService:
    """Service for operations."""

    @staticmethod
    def process_operations(operations: list[list[OperationDto]]) -> list[list[dict]]:
        """
        Gets a list of lists of OperationDto and returns a list of tax results for each operation.
        Returns:
            list: List of lists of OperationTaxDto as dicts.
        """
        try:
            tax_results = []
            for operation_dto_list in operations:                
                operation_taxes = TaxService.calculate_taxes(operation_dto_list)                
                tax_results.append(operation_taxes)
            return tax_results
        except Exception as e:
            raise RuntimeError(f"Error processing operation: {str(e)}")
