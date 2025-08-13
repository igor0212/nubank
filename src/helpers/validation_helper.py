"""
Validation helper functions for data validation and sanitization.
"""
import re
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ValidationHelper:
    """Helper class for data validation operations."""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email (str): Email address to validate
            
        Returns:
            bool: True if email is valid, False otherwise
        """
        if not email or not isinstance(email, str):
            return False
            
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email.strip()))
    
    @staticmethod
    def validate_phone(phone: str, country_code: str = 'BR') -> bool:
        """
        Validate phone number format.
        
        Args:
            phone (str): Phone number to validate
            country_code (str): Country code for validation rules
            
        Returns:
            bool: True if phone is valid, False otherwise
        """
        if not phone or not isinstance(phone, str):
            return False
            
        # Remove all non-digit characters
        clean_phone = re.sub(r'\D', '', phone)
        
        if country_code == 'BR':
            # Brazilian phone validation (10 or 11 digits)
            return len(clean_phone) in [10, 11] and clean_phone.isdigit()
        
        # Generic validation (7-15 digits)
        return 7 <= len(clean_phone) <= 15 and clean_phone.isdigit()
    
    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        """
        Validate Brazilian CPF number.
        
        Args:
            cpf (str): CPF number to validate
            
        Returns:
            bool: True if CPF is valid, False otherwise
        """
        if not cpf or not isinstance(cpf, str):
            return False
            
        # Remove all non-digit characters
        cpf = re.sub(r'\D', '', cpf)
        
        # Check if CPF has 11 digits
        if len(cpf) != 11:
            return False
            
        # Check if all digits are the same
        if cpf == cpf[0] * 11:
            return False
            
        # Validate first check digit
        sum1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digit1 = 11 - (sum1 % 11)
        if digit1 >= 10:
            digit1 = 0
            
        if int(cpf[9]) != digit1:
            return False
            
        # Validate second check digit
        sum2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digit2 = 11 - (sum2 % 11)
        if digit2 >= 10:
            digit2 = 0
            
        return int(cpf[10]) == digit2
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> Dict[str, List[str]]:
        """
        Validate required fields in data dictionary.
        
        Args:
            data (Dict[str, Any]): Data to validate
            required_fields (List[str]): List of required field names
            
        Returns:
            Dict[str, List[str]]: Validation errors
        """
        errors = {'missing_fields': [], 'empty_fields': []}
        
        for field in required_fields:
            if field not in data:
                errors['missing_fields'].append(field)
            elif not data[field] or (isinstance(data[field], str) and not data[field].strip()):
                errors['empty_fields'].append(field)
                
        return errors
    
    @staticmethod
    def validate_string_length(value: str, min_length: int = 0, max_length: int = None) -> bool:
        """
        Validate string length.
        
        Args:
            value (str): String to validate
            min_length (int): Minimum length
            max_length (int): Maximum length
            
        Returns:
            bool: True if length is valid, False otherwise
        """
        if not isinstance(value, str):
            return False
            
        length = len(value.strip())
        
        if length < min_length:
            return False
            
        if max_length is not None and length > max_length:
            return False
            
        return True
    
    @staticmethod
    def validate_numeric_range(value: Union[int, float], min_value: Union[int, float] = None, 
                             max_value: Union[int, float] = None) -> bool:
        """
        Validate numeric value range.
        
        Args:
            value (Union[int, float]): Value to validate
            min_value (Union[int, float]): Minimum value
            max_value (Union[int, float]): Maximum value
            
        Returns:
            bool: True if value is in range, False otherwise
        """
        if not isinstance(value, (int, float)):
            return False
            
        if min_value is not None and value < min_value:
            return False
            
        if max_value is not None and value > max_value:
            return False
            
        return True
    
    @staticmethod
    def validate_date_format(date_string: str, date_format: str = '%Y-%m-%d') -> bool:
        """
        Validate date string format.
        
        Args:
            date_string (str): Date string to validate
            date_format (str): Expected date format
            
        Returns:
            bool: True if date format is valid, False otherwise
        """
        if not date_string or not isinstance(date_string, str):
            return False
            
        try:
            datetime.strptime(date_string, date_format)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = None) -> str:
        """
        Sanitize string by removing dangerous characters and trimming.
        
        Args:
            value (str): String to sanitize
            max_length (int): Maximum length to truncate to
            
        Returns:
            str: Sanitized string
        """
        if not isinstance(value, str):
            return ""
            
        # Remove dangerous characters
        sanitized = re.sub(r'[<>"\']', '', value)
        
        # Trim whitespace
        sanitized = sanitized.strip()
        
        # Truncate if necessary
        if max_length and len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
            
        return sanitized
    
    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, Any]:
        """
        Validate password strength.
        
        Args:
            password (str): Password to validate
            
        Returns:
            Dict[str, Any]: Validation result with strength score and requirements
        """
        if not password or not isinstance(password, str):
            return {
                'is_valid': False,
                'score': 0,
                'requirements': {
                    'min_length': False,
                    'has_uppercase': False,
                    'has_lowercase': False,
                    'has_digit': False,
                    'has_special': False
                }
            }
        
        requirements = {
            'min_length': len(password) >= 8,
            'has_uppercase': bool(re.search(r'[A-Z]', password)),
            'has_lowercase': bool(re.search(r'[a-z]', password)),
            'has_digit': bool(re.search(r'\d', password)),
            'has_special': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        }
        
        score = sum(requirements.values())
        is_valid = score >= 4  # At least 4 out of 5 requirements
        
        return {
            'is_valid': is_valid,
            'score': score,
            'requirements': requirements
        }
