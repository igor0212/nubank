
from src.main.enum.OperationType import OperationType

class OperationDto:
    def __init__(self, operation: str, unit_cost: float, quantity: int):
        # Accept both string and enum for flexibility
        if isinstance(operation, OperationType):
            self.operation = operation
        else:
            self.operation = OperationType(operation)
        self.unit_cost = unit_cost
        self.quantity = quantity

    def to_dict(self):
        return {
            "operation": self.operation.value,
            "unit-cost": self.unit_cost,
            "quantity": self.quantity,
        }
