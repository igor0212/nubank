from src.main.enum.operation_type_enum import OperationTypeEnum

class OperationDto:
    def __init__(self, operation: str, unit_cost: float, quantity: int):
        # Accept both string and enum for flexibility
        if isinstance(operation, OperationTypeEnum):
            self.operation = operation
        else:
            self.operation = OperationTypeEnum(operation)
        self.unit_cost = unit_cost
        self.quantity = quantity

    @staticmethod
    def from_dict(data: dict):
        return OperationDto(
            operation=data.get("operation"),
            unit_cost=data.get("unit-cost"),
            quantity=data.get("quantity"),
        )
    