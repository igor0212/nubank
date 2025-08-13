"""
Operation service for application.
"""

from src.main.dto.OperationTaxDto import OperationTaxDto
from src.main.dto.OperationDto import OperationDto, OperationType

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
            for op_list in operations:
                op_taxes = []
                for op in op_list:                    
                    if op.operation == OperationType.SELL and op.unit_cost > 15:
                        tax = 10000.0
                    else:
                        tax = 0.0
                    op_taxes.append(OperationTaxDto(tax).to_dict())
                tax_results.append(op_taxes)
            return tax_results
        except Exception as e:
            raise Exception(f"Error processing operation: {str(e)}")
        