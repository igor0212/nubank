"""
Custom exception classes for centralized error handling.
"""


class OperationProcessingError(Exception):
    """Exception raised for errors during operation processing."""
    pass


class TaxCalculationError(Exception):
    """Exception raised for errors during tax calculation."""
    pass
