from src.main.enums.operation_type_enum import OperationTypeEnum
from dataclasses import dataclass, field


@dataclass
class OperationDto:
    """
    Data Transfer Object representing a stock market operation (buy or sell).
    """
    operation: OperationTypeEnum = field()
    unit_cost: float = field()
    quantity: int = field()

    def __init__(self, operation: str, unit_cost: float, quantity: int) -> None:
        """
        Initialize an OperationDto.

        Args:
            operation (str or OperationTypeEnum): The type of operation ("buy" or "sell").
            unit_cost (float): The unit cost of the asset.
            quantity (int): The quantity of assets.
        """
        # Accept both string and enum for flexibility
        if isinstance(operation, OperationTypeEnum):
            self.operation = operation
        else:
            self.operation = OperationTypeEnum(operation)
        self.unit_cost = unit_cost
        self.quantity = quantity

    @staticmethod
    def from_dict(data: dict) -> "OperationDto":
        """
        Create an OperationDto from a dictionary.

        Args:
            data (dict): Dictionary with keys "operation", "unit-cost", and "quantity".

        Returns:
            OperationDto: The created OperationDto instance.
        """
        return OperationDto(
            operation=data.get("operation"),
            unit_cost=data.get("unit-cost"),
            quantity=data.get("quantity"),
        )
