"""
Main application entry point.
"""
import logging
from flask import Flask
from config.settings import get_config
from src.main.controller.HealthController import health_bp
from src.main.util.Logger import setup_logging


def create_app() -> Flask:
    """Create and configure Flask application."""
    config = get_config()
    
    # Initialize Flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config.secret_key
    app.config['DEBUG'] = config.debug
    
    # Setup logging
    setup_logging(config.log_level, config.log_format)
    
    # Register blueprints
    app.register_blueprint(health_bp, url_prefix='/api/v1')
    
    return app


def main() -> None:
    """Main application entry point."""
    config = get_config()
    app = create_app()
    
    logging.info(f"Starting {config.app_name} v{config.version}")
    logging.info(f"Environment: {config.environment}")
    
    app.run(
        host=config.host,
        port=config.port,
        debug=config.debug
    )


if __name__ == "__main__":
    main()
