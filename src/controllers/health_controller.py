"""
Health check controller for monitoring application status.
"""
from flask import Blueprint, jsonify, Response
from typing import Dict, Any
import logging
from config.settings import get_config
from src.services.health_service import HealthService

# Create blueprint
health_bp = Blueprint('health', __name__)

# Initialize service
health_service = HealthService()

logger = logging.getLogger(__name__)


@health_bp.route('/health', methods=['GET'])
def health_check() -> Response:
    """
    Health check endpoint.
    
    Returns:
        Response: JSON response with health status
    """
    try:
        health_data = health_service.get_health_status()
        status_code = 200 if health_data['status'] == 'healthy' else 503
        
        logger.info(f"Health check performed: {health_data['status']}")
        return jsonify(health_data), status_code
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': health_service._get_timestamp()
        }), 503


@health_bp.route('/health/detailed', methods=['GET'])
def detailed_health_check() -> Response:
    """
    Detailed health check endpoint with system information.
    
    Returns:
        Response: JSON response with detailed health status
    """
    try:
        health_data = health_service.get_detailed_health_status()
        status_code = 200 if health_data['status'] == 'healthy' else 503
        
        logger.info(f"Detailed health check performed: {health_data['status']}")
        return jsonify(health_data), status_code
        
    except Exception as e:
        logger.error(f"Detailed health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': health_service._get_timestamp()
        }), 503


@health_bp.route('/version', methods=['GET'])
def get_version() -> Response:
    """
    Get application version information.
    
    Returns:
        Response: JSON response with version information
    """
    try:
        config = get_config()
        version_data = {
            'name': config.app_name,
            'version': config.version,
            'environment': config.environment,
            'timestamp': health_service._get_timestamp()
        }
        
        logger.info("Version information requested")
        return jsonify(version_data), 200
        
    except Exception as e:
        logger.error(f"Version check failed: {str(e)}")
        return jsonify({
            'error': str(e),
            'timestamp': health_service._get_timestamp()
        }), 500
