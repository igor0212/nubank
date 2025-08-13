"""
Operation service for application.
"""

import json

class OperationService:
    """Service for operations."""

    def processOperations(self, operations: list) -> list:
        """
        Gets a list of operations and processes them.
        
        Returns:
            list: List of processed operations.
        """
        try:
            print(json.dumps({"received": operations}))
            return operations
        except Exception as e:            
            raise Exception(f"Error processing operation: {str(e)}")
            raise Exception(f"Error processing operation: {str(e)}")
           
   