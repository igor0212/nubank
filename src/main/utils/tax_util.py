"""
Tax util for application. It provides utility functions for processing tax-related data.
"""
from src.main.config.tax_config import ZERO
from src.main.dto.operation_dto import OperationDto


class TaxUtil:
    """
    Utility class for formatting and processing tax input data.
    """

    @staticmethod
    def process_buy_operation(weighted_avg, total_qty, op: OperationDto) -> tuple:
        """
        Processes a buy operation. Gets the weighted average cost and total quantity for buy operations.
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
    def validate_sell_quantity(requested_qty, total_qty) -> int:
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
    def calculate_transaction_total_value(unit_cost, quantity) -> float:
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
    def calculate_profit(unit_cost, weighted_avg, quantity) -> float:
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
    def deduct_accumulated_loss(taxable_profit, accumulated_loss) -> tuple:
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
