class OperationTaxDto:
    def __init__(self, tax: float) -> None:
        self.tax = tax

    def to_dict(self) -> dict:
        return {"tax": self.tax}
