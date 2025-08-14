"""
Operation service for application.
"""

from src.main.dto.OperationDto import OperationDto
from src.main.service.TaxService import TaxService

class OperationService:
    """Service for operations."""

    @staticmethod
    def processOperations(operations: list[list[OperationDto]]) -> list[list[dict]]:
        """
        Gets a list of lists of OperationDto and returns a list of tax results for each operation.
        Returns:
            list: List of lists of OperationTaxDto as dicts.
        """
        try:
            tax_results = []
            for operationDtoList in operations:                
                operation_taxes = TaxService.calculateTaxes(operationDtoList)                
                tax_results.append(operation_taxes)
            return tax_results
        except Exception as e:
            raise Exception(f"Error processing operation: {str(e)}")
