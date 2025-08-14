from dataclasses import dataclass


@dataclass
class OperationTaxDto:
    """
    Data Transfer Object representing the tax result for an operation.
    """
    tax: float

    def to_dict(self) -> dict:
        """
        Convert the OperationTaxDto to a dictionary.

        Returns:
            dict: Dictionary with the tax value.
        """
        return {"tax": self.tax}
