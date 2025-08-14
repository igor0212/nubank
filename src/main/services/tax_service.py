"""
Tax service for application.
Provides methods to calculate taxes for stock market operations according to business rules.
"""
from src.main.config.tax_config import TAX_PERCENTAGE, ZERO, TOTAL_VALUE_TRANSACTION_WITH_NO_TAX
from src.main.enums.operation_type_enum import OperationTypeEnum
from src.main.exceptions.exception import TaxCalculationError
from src.main.dto.operation_dto import OperationDto
from src.main.dto.operation_tax_dto import OperationTaxDto
from src.main.utils.tax_util import TaxUtil


class TaxService:
    """
    Service for taxes.
    Calculates taxes for a list of operations, considering weighted average, accumulated loss, and business rules.
    Allows dependency injection for configuration.
    """

    def __init__(self, tax_percentage: float = TAX_PERCENTAGE, total_value_transaction_with_no_tax: float = TOTAL_VALUE_TRANSACTION_WITH_NO_TAX):
        """
        Args:
            tax_percentage (float): The tax percentage to apply on profits.
            total_value_transaction_with_no_tax (float): The maximum transaction value to does not apply tax.
        """
        self.tax_percentage = tax_percentage
        self.total_value_transaction_with_no_tax = total_value_transaction_with_no_tax

    def calculate_taxes(self, operations: list[OperationDto]) -> list[OperationTaxDto]:
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
                    weighted_avg, total_qty = TaxUtil.update_weighted_avg(
                        weighted_avg, total_qty, op)
                elif op.operation == OperationTypeEnum.SELL:
                    tax, weighted_avg, total_qty, accumulated_loss = self.__process_sell(
                        op, weighted_avg, total_qty, accumulated_loss
                    )

                taxes.append(OperationTaxDto(tax).to_dict())
        except Exception as e:
            raise TaxCalculationError(str(e))

        return taxes

    def __process_sell(self, op: OperationDto, weighted_avg, total_qty, accumulated_loss):
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
        sell_qty = TaxUtil.get_sell_quantity(op.quantity, total_qty)
        total_qty -= sell_qty
        total_value = TaxUtil.calculate_total_value(
            op.unit_cost, sell_qty)
        profit = TaxUtil.calculate_profit(
            op.unit_cost, weighted_avg, sell_qty)

        taxable_profit = profit

        # Should not deduct the profit obtained from accumulated losses if the total
        # value of the transaction is less than or equal to total_value_transaction
        if accumulated_loss < 0 and total_value > self.total_value_transaction_with_no_tax:
            taxable_profit, accumulated_loss = TaxUtil.deduct_accumulated_loss(
                taxable_profit, accumulated_loss)
        tax, accumulated_loss = self.__calculate_tax(
            total_value, taxable_profit, profit, accumulated_loss
        )
        return tax, weighted_avg, total_qty, accumulated_loss

    def __calculate_tax(self, total_value, taxable_profit, profit, accumulated_loss):
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
        if total_value <= self.total_value_transaction_with_no_tax or taxable_profit <= 0:
            if profit < 0:
                accumulated_loss += profit
        else:
            tax = round(taxable_profit * self.tax_percentage, 2)
        return tax, accumulated_loss
