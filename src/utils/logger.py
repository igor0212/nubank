"""
Logging utility functions and configuration.
"""
import logging
import logging.config
import sys
from typing import Dict, Any
import structlog
from datetime import datetime


def setup_logging(log_level: str = "INFO", log_format: str = "json") -> None:
    """
    Setup application logging configuration.
    
    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format (str): Log format type ('json' or 'text')
    """
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if log_format == "json" else structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard logging
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                'format': '%(asctime)s %(name)s %(levelname)s %(message)s',
                'class': 'pythonjsonlogger.jsonlogger.JsonFormatter'
            },
            'text': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': log_level,
                'formatter': log_format,
                'stream': sys.stdout
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': log_level,
                'formatter': log_format,
                'filename': 'logs/app.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            }
        },
        'loggers': {
            '': {  # root logger
                'level': log_level,
                'handlers': ['console', 'file'],
                'propagate': False
            },
            'src': {
                'level': log_level,
                'handlers': ['console', 'file'],
                'propagate': False
            }
        }
    }
    
    # Create logs directory if it doesn't exist
    import os
    os.makedirs('logs', exist_ok=True)
    
    logging.config.dictConfig(logging_config)


class LoggerMixin:
    """Mixin class to add logging capabilities to any class."""
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger instance for the class."""
        return logging.getLogger(self.__class__.__module__ + '.' + self.__class__.__name__)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name (str): Logger name
        
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)


def log_function_call(func):
    """
    Decorator to log function calls with parameters and execution time.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        start_time = datetime.now()
        
        # Log function entry
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        
        try:
            result = func(*args, **kwargs)
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Log successful completion
            logger.debug(f"{func.__name__} completed successfully in {execution_time:.3f}s")
            return result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Log exception
            logger.error(f"{func.__name__} failed after {execution_time:.3f}s: {str(e)}")
            raise
            
    return wrapper


def log_performance(operation_name: str):
    """
    Decorator to log performance metrics for operations.
    
    Args:
        operation_name (str): Name of the operation being measured
        
    Returns:
        Decorator function
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__module__)
            start_time = datetime.now()
            
            try:
                result = func(*args, **kwargs)
                execution_time = (datetime.now() - start_time).total_seconds()
                
                # Log performance metrics
                logger.info(f"Performance: {operation_name} completed in {execution_time:.3f}s")
                return result
                
            except Exception as e:
                execution_time = (datetime.now() - start_time).total_seconds()
                logger.error(f"Performance: {operation_name} failed after {execution_time:.3f}s: {str(e)}")
                raise
                
        return wrapper
    return decorator


class StructuredLogger:
    """Structured logger wrapper for consistent logging format."""
    
    def __init__(self, name: str):
        """
        Initialize structured logger.
        
        Args:
            name (str): Logger name
        """
        self.logger = structlog.get_logger(name)
    
    def info(self, message: str, **kwargs) -> None:
        """Log info message with structured data."""
        self.logger.info(message, **kwargs)
    
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message with structured data."""
        self.logger.debug(message, **kwargs)
    
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message with structured data."""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs) -> None:
        """Log error message with structured data."""
        self.logger.error(message, **kwargs)
    
    def critical(self, message: str, **kwargs) -> None:
        """Log critical message with structured data."""
        self.logger.critical(message, **kwargs)
    
    def bind(self, **kwargs) -> 'StructuredLogger':
        """
        Bind context data to logger.
        
        Returns:
            StructuredLogger: New logger instance with bound context
        """
        bound_logger = self.logger.bind(**kwargs)
        new_instance = StructuredLogger.__new__(StructuredLogger)
        new_instance.logger = bound_logger
        return new_instance


def create_audit_log(user_id: str, action: str, resource: str, details: Dict[str, Any] = None) -> None:
    """
    Create audit log entry.
    
    Args:
        user_id (str): ID of the user performing the action
        action (str): Action being performed
        resource (str): Resource being acted upon
        details (Dict[str, Any]): Additional details about the action
    """
    audit_logger = StructuredLogger('audit')
    audit_logger.info(
        "Audit log entry",
        user_id=user_id,
        action=action,
        resource=resource,
        details=details or {},
        timestamp=datetime.utcnow().isoformat()
    )
