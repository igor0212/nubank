"""
Tax service for application.
Provides methods to calculate taxes for stock market operations according to business rules.
"""
from src.main.config.tax_config import TAX_PERCENTAGE, ZERO, TOTAL_VALUE_TRANSACTION
from src.main.enum.operation_type_enum import OperationTypeEnum
from src.main.dto.operation_dto import OperationDto
from src.main.dto.operation_tax_dto import OperationTaxDto

class TaxService:
    """
    Service for taxes.
    Calculates taxes for a list of operations, considering weighted average, accumulated loss, and business rules.
    """    

    @staticmethod
    def calculate_taxes(operations: list[OperationDto]) -> list[OperationTaxDto]:
        """
        Calculates the tax for each operation in the list, following the business rules.
        Args:
            operations (list[OperationDto]): List of operations to process.
        Returns:
            list: List of tax values (OperationTaxDto) for each operation.
        """
        taxes = []
        weighted_avg = ZERO
        total_qty = 0
        accumulated_loss = ZERO

        try:
            for op in operations:
                tax = ZERO
                if op.operation == OperationTypeEnum.BUY:
                    weighted_avg, total_qty = TaxService.__update_weighted_avg(weighted_avg, total_qty, op)                
                elif op.operation == OperationTypeEnum.SELL:
                    tax, weighted_avg, total_qty, accumulated_loss = TaxService.__process_sell(
                        op, weighted_avg, total_qty, accumulated_loss
                    )
            
                taxes.append(OperationTaxDto(tax).to_dict())
        except Exception as e:
            raise ValueError(str(e))
        
        return taxes

    @staticmethod
    def __update_weighted_avg(weighted_avg, total_qty, op: OperationDto):
        """
        Updates the weighted average cost and total quantity for buy operations.
        Args:
            weighted_avg (float): Current weighted average.
            total_qty (int): Current total quantity.
            op (OperationDto): The buy operation.
        Returns:
            tuple: (weighted_avg, total_qty)
        """
        total_cost = weighted_avg * total_qty + op.unit_cost * op.quantity
        total_qty += op.quantity
        weighted_avg = total_cost / total_qty if total_qty > 0 else ZERO
        return weighted_avg, total_qty

    @staticmethod
    def __process_sell(op: OperationDto, weighted_avg, total_qty, accumulated_loss):
        """
        Processes a sell operation, updating quantities, accumulated loss, and calculating tax.
        Args:
            op (OperationDto): The sell operation.
            weighted_avg (float): Current weighted average.
            total_qty (int): Current total quantity.
            accumulated_loss (float): Current accumulated loss.
        Returns:
            tuple: (tax, weighted_avg, total_qty, accumulated_loss)
        """
        sell_qty = TaxService.__get_sell_quantity(op.quantity, total_qty)
        total_qty -= sell_qty
        total_value = TaxService.__calculate_total_value(op.unit_cost, sell_qty)
        profit = TaxService.__calculate_profit(op.unit_cost, weighted_avg, sell_qty)

        taxable_profit = profit

        # Should not deduct the profit obtained from accumulated losses if the total
        # value of the transaction is less than or equal to 20000.00
        if accumulated_loss < 0 and total_value > TOTAL_VALUE_TRANSACTION:
            taxable_profit, accumulated_loss = TaxService.__deduct_accumulated_loss(taxable_profit, accumulated_loss)
        tax, accumulated_loss = TaxService.__calculate_tax(
            total_value, taxable_profit, profit, accumulated_loss
        )
        return tax, weighted_avg, total_qty, accumulated_loss

    @staticmethod
    def __get_sell_quantity(requested_qty, total_qty):
        """
        Validates if the selling quantity is greater than the total quantity.
        Args:
            requested_qty (int): Quantity requested to sell.
            total_qty (int): Current total quantity.
        Returns:
            int: The validated selling quantity.
        """        
        return min(requested_qty, total_qty)

    @staticmethod
    def __calculate_total_value(unit_cost, quantity):
        """
        Calculates the total value of a transaction.
        Args:
            unit_cost (float): Unit cost of the asset.
            quantity (int): Quantity of assets.
        Returns:
            float: The total value of the transaction.
        """
        return unit_cost * quantity

    @staticmethod
    def __calculate_profit(unit_cost, weighted_avg, quantity):
        """
        Calculates the profit for a given transaction.
        Args:
            unit_cost (float): Unit cost of the asset.
            weighted_avg (float): Weighted average cost.
            quantity (int): Quantity of assets.
        Returns:
            float: The profit for the transaction.
        """
        return (unit_cost - weighted_avg) * quantity

    @staticmethod
    def __deduct_accumulated_loss(taxable_profit, accumulated_loss):
        """
        Deducts the accumulated loss from the profit if applicable.        
        Args:
            taxable_profit (float): Current taxable profit.
            accumulated_loss (float): Current accumulated loss.
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
    def __calculate_tax(total_value, taxable_profit, profit, accumulated_loss):
        """
        Calculates the tax based on the provided parameters.
        Args:
            total_value (float): Total value of the transaction.
            taxable_profit (float): Taxable profit after deductions.
            profit (float): Profit for the transaction.
            accumulated_loss (float): Current accumulated loss.
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
