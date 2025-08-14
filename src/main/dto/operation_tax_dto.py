class OperationTaxDto:
    def __init__(self, tax: float):
        self.tax = tax

    def to_dict(self):
        return {"tax": self.tax}
