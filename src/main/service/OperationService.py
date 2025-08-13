"""
Operation service for application.
"""

from src.main.dto.OperationTaxDto import OperationTaxDto
from src.main.dto.OperationDto import OperationDto


class OperationService:
    """Service for operations."""

    @staticmethod
    def processOperations(operationsList: list[list[OperationDto]]) -> list[list[OperationTaxDto]]:
        """
        Gets a list of lists of OperationDto and returns a list of tax results for each operation.
        Returns:
            list: List of lists of OperationTaxDto as dicts.
        """
        try:
            taxResultsList = []
            for operationDtoList in operationsList:
                if(len(operationDtoList) == 0):                    
                    continue
                
                operationTaxDtoList = []
                for operationDto in operationDtoList:                    
                    if operationDto.operation == "sell" and operationDto.unit_cost > 15:
                        tax = 10000.0
                    else:
                        tax = 0.0
                    operationTaxDtoList.append(OperationTaxDto(tax).to_dict())
                taxResultsList.append(operationTaxDtoList)
            return taxResultsList
        except Exception as e:
            raise Exception(f"Error processing operation: {str(e)}")

