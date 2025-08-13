"""
Main application entry point.
"""
import logging
from config.Settings import get_config
from controller.HealthController import health_bp
from util.Logger import setup_logging
from flask import Flask, request, jsonify


def create_app() -> 'Flask':
    """Create and configure Flask application."""
    config = get_config()
    
    # Initialize Flask app
    app = Flask(__name__)    
    app.config['DEBUG'] = config.debug
    
    # Setup logging
    setup_logging(config.log_level, config.log_format)
    
    # Register blueprints
    app.register_blueprint(health_bp, url_prefix='/api/v1')

    @app.route('/api/v1/operations', methods=['GET'])
    def operations():
        """
        Accepts a JSON array of operations and returns a simple acknowledgment.
        Example input:
        [
            {"operation":"buy", "unit-cost":10.00, "quantity": 10000},
            {"operation":"sell", "unit-cost":20.00, "quantity": 5000}
        ]
        """
        data = request.get_json(force=True)
        # Here you can process the data as needed
        # For now, just echo back the received data
        return jsonify({"received": data}), 200

    return app


def main() -> None:
    """Main application entry point."""
    config = get_config()
    app = create_app()
    
    logging.info(f"Starting {config.app_name} v{config.version}")
    logging.info(f"Environment: {config.environment}")
    
    app.run(
        debug=config.debug
    )


if __name__ == "__main__":
    main()
