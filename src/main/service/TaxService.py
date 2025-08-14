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
        Calculates the tax for each operation in the list, following the business rules:
        - Tax is 20% over the profit of a sell operation, if the sell price > weighted average buy price.
        - Weighted average price is recalculated on each buy.
        - Losses are accumulated and used to offset future profits.
        - No tax is paid if the total value of the sell operation (unit_cost * quantity) <= 20000.
        - No tax is paid on buy operations.
        Returns:
            list: List of tax values (OperationTaxDto) for each operation.
        """
        taxes = []
        weighted_avg = ZERO
        total_qty = 0
        accumulated_loss = ZERO

        for op in operations:
            if op.operation == OperationType.BUY:                
                # Recalculate weighted average price
                total_cost = weighted_avg * total_qty + op.unit_cost * op.quantity
                total_qty += op.quantity
                weighted_avg = total_cost / total_qty if total_qty > 0 else ZERO
                taxes.append(OperationTaxDto(ZERO).toDict())
            elif op.operation == OperationType.SELL:
                if op.quantity > total_qty:
                    # Selling more than you have, treat as error or sell only what you have
                    sell_qty = total_qty
                else:
                    sell_qty = op.quantity

                total_qty -= sell_qty

                total_value = op.unit_cost * sell_qty
                profit = (op.unit_cost - weighted_avg) * sell_qty

                # Deduct accumulated loss from profit if total operation value > 20000 
                taxable_profit = profit
                if accumulated_loss < 0 and total_value > TOTAL_VALUE_TRANSACTION:
                    taxable_profit += accumulated_loss
                    if taxable_profit > 0:
                        accumulated_loss = ZERO
                    else:
                        accumulated_loss = taxable_profit
                        taxable_profit = ZERO                

                # No tax if total operation value <= 20000
                if total_value <= TOTAL_VALUE_TRANSACTION or taxable_profit <= 0:
                    if profit < 0:
                        accumulated_loss += profit                    
                    taxes.append(OperationTaxDto(ZERO).toDict())
                else:
                    tax = taxable_profit * TAX_PERCENTAGE                    
                    taxes.append(OperationTaxDto(round(tax, 2)).toDict())
            else:                
                taxes.append(OperationTaxDto(ZERO).toDict())

        return taxes