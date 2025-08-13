"""
Health service for application health monitoring.
"""
import platform
from datetime import datetime
from typing import Dict, Any
import logging
from config.Settings import get_config

logger = logging.getLogger(__name__)


class HealthService:
    """Service for handling health check operations."""
    
    def __init__(self):
        """Initialize health service."""
        self.config = get_config()
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get basic health status.
        
        Returns:
            Dict[str, Any]: Basic health status information
        """
        try:
            return {
                'status': 'healthy',
                'timestamp': self._get_timestamp(),
                'version': self.config.version,
                'environment': self.config.environment
            }
        except Exception as e:
            logger.error(f"Error getting health status: {str(e)}")
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': self._get_timestamp()
            }
    
    def get_detailed_health_status(self) -> Dict[str, Any]:
        """
        Get detailed health status with system information.
        
        Returns:
            Dict[str, Any]: Detailed health status information
        """
        try:
            system_info = self._get_system_info()
            memory_info = self._get_memory_info()
            disk_info = self._get_disk_info()
            
            return {
                'status': 'healthy',
                'timestamp': self._get_timestamp(),
                'version': self.config.version,
                'environment': self.config.environment,
                'system': system_info,
                'memory': memory_info,
                'disk': disk_info,
                'uptime': self._get_uptime()
            }
        except Exception as e:
            logger.error(f"Error getting detailed health status: {str(e)}")
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': self._get_timestamp()
            }
    
    def _get_timestamp(self) -> str:
        """
        Get current timestamp in ISO format.
        
        Returns:
            str: Current timestamp
        """
        return datetime.utcnow().isoformat() + 'Z'
    
    def _get_system_info(self) -> Dict[str, Any]:
        """
        Get system information.
        
        Returns:
            Dict[str, Any]: System information
        """
        return {
            'platform': platform.platform(),
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version()            
        }  
    