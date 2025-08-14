import unittest
from src.main.utils.tax_util import TaxUtil
from src.main.dto.operation_dto import OperationDto
from src.main.enums.operation_type_enum import OperationTypeEnum


class TestTaxUtil(unittest.TestCase):
    def test_process_buy_operation(self):
        op = OperationDto(OperationTypeEnum.BUY, 10.0, 100)
        weighted_avg, total_qty = TaxUtil.process_buy_operation(
            0.0, 0, op)
        self.assertEqual(weighted_avg, 10.0)
        self.assertEqual(total_qty, 100)

        op2 = OperationDto(OperationTypeEnum.BUY, 20.0, 100)
        weighted_avg2, total_qty2 = TaxUtil.process_buy_operation(
            weighted_avg, total_qty, op2)
        self.assertEqual(weighted_avg2, 15.0)
        self.assertEqual(total_qty2, 200)

    def test_validate_sell_quantity(self):
        self.assertEqual(TaxUtil.validate_sell_quantity(10, 20), 10)
        self.assertEqual(TaxUtil.validate_sell_quantity(30, 20), 20)

    def test_calculate_transaction_total_value(self):
        self.assertEqual(
            TaxUtil.calculate_transaction_total_value(10.0, 5), 50.0)

    def test_calculate_profit(self):
        self.assertEqual(TaxUtil.calculate_profit(20.0, 10.0, 5), 50.0)
        self.assertEqual(TaxUtil.calculate_profit(5.0, 10.0, 5), -25.0)

    def test_deduct_accumulated_loss(self):
        taxable_profit, accumulated_loss = TaxUtil.deduct_accumulated_loss(
            100.0, -50.0)
        self.assertEqual(taxable_profit, 50.0)
        self.assertEqual(accumulated_loss, 0.0)

        taxable_profit, accumulated_loss = TaxUtil.deduct_accumulated_loss(
            30.0, -50.0)
        self.assertEqual(taxable_profit, 0.0)
        self.assertEqual(accumulated_loss, -20.0)


if __name__ == "__main__":
    unittest.main()
