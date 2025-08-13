class OperationTaxDto:
    def __init__(self, tax: float):
        self.tax = tax

    def toDict(self):
        return {"tax": self.tax}
