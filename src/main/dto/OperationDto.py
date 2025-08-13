class OperationDto:
    def __init__(self, operation: str, unit_cost: float, quantity: int):
        self.operation = operation
        self.unit_cost = unit_cost
        self.quantity = quantity

    @staticmethod
    def from_dict(data: dict):
        return OperationDto(
            operation=data.get("operation"),
            unit_cost=data.get("unit-cost"),
            quantity=data.get("quantity"),
        )

    def to_dict(self):
        return {
            "operation": self.operation,
            "unit-cost": self.unit_cost,
            "quantity": self.quantity,
        }
