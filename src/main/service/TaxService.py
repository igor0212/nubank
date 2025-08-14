"""
Tax service for application.
"""
from src.main.config.TaxConfig import TAX_PERCENTAGE, ZERO, TOTAL_VALUE_TRANSACTION
from src.main.enum.OperationType import OperationType
from src.main.dto.OperationDto import OperationDto
from src.main.dto.OperationTaxDto import OperationTaxDto

class TaxService:
    """Service for taxes."""    

    @staticmethod
    def calculateTaxes(operations: list[OperationDto]) -> list[OperationTaxDto]:
        """
        Calculates the tax for each operation in the list, following the business rules.
        Returns:
            list: List of tax values (OperationTaxDto) for each operation.
        """
        taxes = []
        weighted_avg = ZERO
        total_qty = 0
        accumulated_loss = ZERO

        for op in operations:
            tax = ZERO
            if op.operation == OperationType.BUY:
                weighted_avg, total_qty = TaxService.__updateWeightedAvg(weighted_avg, total_qty, op)                
            elif op.operation == OperationType.SELL:
                tax, weighted_avg, total_qty, accumulated_loss = TaxService.__processSell(
                    op, weighted_avg, total_qty, accumulated_loss
                )                
            
            taxes.append(OperationTaxDto(tax).toDict())

        return taxes

    @staticmethod
    def __updateWeightedAvg(weighted_avg, total_qty, op: OperationDto):
        """
        Updates the weighted average cost and total quantity for buy operations.
        Returns:
            tuple: (weighted_avg, total_qty)
        """
        total_cost = weighted_avg * total_qty + op.unit_cost * op.quantity
        total_qty += op.quantity
        weighted_avg = total_cost / total_qty if total_qty > 0 else ZERO
        return weighted_avg, total_qty

    @staticmethod
    def __processSell(op: OperationDto, weighted_avg, total_qty, accumulated_loss):
        """
        Processes a sell operation.
        Returns:
            tuple: (tax, weighted_avg, total_qty, accumulated_loss)
        """
        sell_qty = TaxService.__getSellQuantity(op.quantity, total_qty)
        total_qty -= sell_qty
        total_value = TaxService.__calculateTotalValue(op.unit_cost, sell_qty)
        profit = TaxService.__calculateProfit(op.unit_cost, weighted_avg, sell_qty)

        taxable_profit = profit
        
        # Should not deduct the profit obtained from accumulated losses if the total
        # value of the transaction is less than or equal to 20000.00
        if accumulated_loss < 0 and total_value > TOTAL_VALUE_TRANSACTION:
            taxable_profit, accumulated_loss = TaxService.__deductAccumulatedLoss(taxable_profit, accumulated_loss)
        tax, accumulated_loss = TaxService.__calculateTax(
            total_value, taxable_profit, profit, accumulated_loss
        )
        return tax, weighted_avg, total_qty, accumulated_loss

    @staticmethod
    def __getSellQuantity(requested_qty, total_qty):
        """
        Validating if the selling quantity is greater than the total quantity
        Returns:
            int: The validated selling quantity
        """        
        return min(requested_qty, total_qty)

    @staticmethod
    def __calculateTotalValue(unit_cost, quantity):
        """
        Calculates the total value of a transaction.
        Returns:
            int: The total value of the transaction
        """
        return unit_cost * quantity

    @staticmethod
    def __calculateProfit(unit_cost, weighted_avg, quantity):
        """
        Calculates the profit for a given transaction.
        Returns:
            int: The profit for the transaction
        """
        return (unit_cost - weighted_avg) * quantity

    @staticmethod
    def __deductAccumulatedLoss(taxable_profit, accumulated_loss):
        """
        Deducts the accumulated loss from the profit if applicable.        
        Returns:
            tuple: (taxable_profit, accumulated_loss)
        """        
        taxable_profit += accumulated_loss
        if taxable_profit > 0:
            accumulated_loss = ZERO
        else:
            accumulated_loss = taxable_profit
            taxable_profit = ZERO
        return taxable_profit, accumulated_loss

    @staticmethod
    def __calculateTax(total_value, taxable_profit, profit, accumulated_loss):
        """
        Calculates the tax based on the provided parameters.
        Returns:
            tuple: (tax, accumulated_loss)
        """
        tax = ZERO
        if total_value <= TOTAL_VALUE_TRANSACTION or taxable_profit <= 0:
            if profit < 0:
                accumulated_loss += profit
        else:
            tax = round(taxable_profit * TAX_PERCENTAGE, 2)
        return tax, accumulated_loss


