class OperationTaxDto:
    """
    Data Transfer Object representing the tax result for an operation.
    """

    def __init__(self, tax: float) -> None:
        """
        Initialize an OperationTaxDto.

        Args:
            tax (float): The tax value for the operation.
        """
        self.tax = tax

    def to_dict(self) -> dict:
        """
        Convert the OperationTaxDto to a dictionary.

        Returns:
            dict: Dictionary with the tax value.
        """
        return {"tax": self.tax}
