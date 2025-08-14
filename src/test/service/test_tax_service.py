import unittest
from src.main.service.tax_service import TaxService
from src.main.enums.operation_type_enum import OperationTypeEnum
from src.main.dto.operation_dto import OperationDto


class TestTaxService(unittest.TestCase):
    def check_calculate_taxes(self, operations, expected):
        # When
        actual = TaxService.calculate_taxes(operations)

        # Then
        self.assertEqual(actual, expected)

    def test_calculate_tax_case_1(self):
        # Given
        operations = [
            OperationDto(OperationTypeEnum.BUY, 10.00, 100),
            OperationDto(OperationTypeEnum.SELL, 15.00, 50),
            OperationDto(OperationTypeEnum.SELL, 15.00, 50)
        ]

        expected = [{"tax": 0.0}, {"tax": 0.0}, {"tax": 0.0}]

        self.check_calculate_taxes(operations, expected)

    def test_calculate_tax_case_2(self):
        # Given
        operations = [
            OperationDto(OperationTypeEnum.BUY, 10.00, 10000),
            OperationDto(OperationTypeEnum.SELL, 20.00, 5000),
            OperationDto(OperationTypeEnum.SELL, 5.00, 5000)
        ]

        expected = [{"tax": 0.0}, {"tax": 10000.0}, {"tax": 0.0}]

        self.check_calculate_taxes(operations, expected)

    def test_calculate_tax_case_3(self):
        # Given
        operations = [
            OperationDto(OperationTypeEnum.BUY, 10.00, 10000),
            OperationDto(OperationTypeEnum.SELL, 5.00, 5000),
            OperationDto(OperationTypeEnum.SELL, 20.00, 3000)
        ]

        expected = [{"tax": 0.0}, {"tax": 0.0}, {"tax": 1000.0}]

        self.check_calculate_taxes(operations, expected)

    def test_calculate_tax_case_4(self):
        # Given
        operations = [
            OperationDto(OperationTypeEnum.BUY, 10.00, 10000),
            OperationDto(OperationTypeEnum.BUY, 25.00, 5000),
            OperationDto(OperationTypeEnum.SELL, 15.00, 10000)
        ]

        expected = [{"tax": 0.0}, {"tax": 0.0}, {"tax": 0.0}]

        self.check_calculate_taxes(operations, expected)

    def test_calculate_tax_case_5(self):
        # Given
        operations = [
            OperationDto(OperationTypeEnum.BUY, 10.00, 10000),
            OperationDto(OperationTypeEnum.BUY, 25.00, 5000),
            OperationDto(OperationTypeEnum.SELL, 15.00, 10000),
            OperationDto(OperationTypeEnum.SELL, 25.00, 5000)
        ]

        expected = [{"tax": 0.0}, {"tax": 0.0}, {"tax": 0.0}, {"tax": 10000.0}]

        self.check_calculate_taxes(operations, expected)

    def test_calculate_tax_case_6(self):
        # Given
        operations = [
            OperationDto(OperationTypeEnum.BUY, 10.00, 10000),
            OperationDto(OperationTypeEnum.SELL, 2.00, 5000),
            OperationDto(OperationTypeEnum.SELL, 20.00, 2000),
            OperationDto(OperationTypeEnum.SELL, 20.00, 2000),
            OperationDto(OperationTypeEnum.SELL, 25.00, 1000)
        ]

        expected = [{"tax": 0.0}, {"tax": 0.0}, {
            "tax": 0.0}, {"tax": 0.0}, {"tax": 3000.0}]

        self.check_calculate_taxes(operations, expected)

    def test_calculate_tax_case_7(self):
        # Given
        operations = [
            OperationDto(OperationTypeEnum.BUY, 10.00, 10000),
            OperationDto(OperationTypeEnum.SELL, 2.00, 5000),
            OperationDto(OperationTypeEnum.SELL, 20.00, 2000),
            OperationDto(OperationTypeEnum.SELL, 20.00, 2000),
            OperationDto(OperationTypeEnum.SELL, 25.00, 1000),
            OperationDto(OperationTypeEnum.BUY, 20.00, 10000),
            OperationDto(OperationTypeEnum.SELL, 15.00, 5000),
            OperationDto(OperationTypeEnum.SELL, 30.00, 4350),
            OperationDto(OperationTypeEnum.SELL, 30.00, 650)
        ]

        expected = [{"tax": 0.0}, {"tax": 0.0}, {"tax": 0.0}, {"tax": 0.0}, {
            "tax": 3000.0}, {"tax": 0.0}, {"tax": 0.0}, {"tax": 3700.0}, {"tax": 0.0}]

        self.check_calculate_taxes(operations, expected)

    def test_calculate_tax_case_8(self):
        # Given
        operations = [
            OperationDto(OperationTypeEnum.BUY, 10.00, 10000),
            OperationDto(OperationTypeEnum.SELL, 50.00, 10000),
            OperationDto(OperationTypeEnum.BUY, 20.00, 10000),
            OperationDto(OperationTypeEnum.SELL, 50.00, 10000)
        ]

        expected = [{"tax": 0.0}, {"tax": 80000.0},
                    {"tax": 0.0}, {"tax": 60000.0}]

        self.check_calculate_taxes(operations, expected)

    def test_calculate_tax_case_9(self):
        # Given
        operations = [
            OperationDto(OperationTypeEnum.BUY, 5000.00, 10),
            OperationDto(OperationTypeEnum.SELL, 4000.00, 5),
            OperationDto(OperationTypeEnum.BUY, 15000.00, 5),
            OperationDto(OperationTypeEnum.BUY, 4000.00, 2),
            OperationDto(OperationTypeEnum.BUY, 23000.00, 2),
            OperationDto(OperationTypeEnum.SELL, 20000.00, 1),
            OperationDto(OperationTypeEnum.SELL, 12000.00, 10),
            OperationDto(OperationTypeEnum.SELL, 15000.00, 3)
        ]

        expected = [{"tax": 0.0}, {"tax": 0.0}, {"tax": 0.0}, {"tax": 0.0}, {
            "tax": 0.0}, {"tax": 0.0}, {"tax": 1000.0}, {"tax": 2400.0}]

        self.check_calculate_taxes(operations, expected)


if __name__ == "__main__":
    unittest.main()
