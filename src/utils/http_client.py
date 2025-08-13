"""
HTTP client utility for making external API requests.
"""
import requests
from typing import Dict, Any, Optional, Union
import logging
from datetime import datetime, timedelta
import time
from config.settings import get_config

logger = logging.getLogger(__name__)


class HTTPClient:
    """HTTP client with retry logic, timeout handling, and logging."""
    
    def __init__(self, base_url: str = None, timeout: int = None, max_retries: int = None):
        """
        Initialize HTTP client.
        
        Args:
            base_url (str): Base URL for all requests
            timeout (int): Request timeout in seconds
            max_retries (int): Maximum number of retry attempts
        """
        config = get_config()
        self.base_url = base_url or ""
        self.timeout = timeout or config.api_timeout
        self.max_retries = max_retries or config.max_retries
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': f'{config.app_name}/{config.version}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Make HTTP request with retry logic.
        
        Args:
            method (str): HTTP method
            url (str): Request URL
            **kwargs: Additional request parameters
            
        Returns:
            requests.Response: HTTP response
            
        Raises:
            requests.RequestException: If request fails after all retries
        """
        full_url = f"{self.base_url.rstrip('/')}/{url.lstrip('/')}" if self.base_url else url
        
        for attempt in range(self.max_retries + 1):
            try:
                start_time = datetime.now()
                
                response = self.session.request(
                    method=method,
                    url=full_url,
                    timeout=self.timeout,
                    **kwargs
                )
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                logger.info(
                    f"HTTP {method} {full_url} - Status: {response.status_code} - "
                    f"Time: {execution_time:.3f}s - Attempt: {attempt + 1}"
                )
                
                # Raise exception for HTTP error status codes
                response.raise_for_status()
                return response
                
            except requests.exceptions.RequestException as e:
                execution_time = (datetime.now() - start_time).total_seconds()
                
                if attempt == self.max_retries:
                    logger.error(
                        f"HTTP {method} {full_url} failed after {attempt + 1} attempts - "
                        f"Time: {execution_time:.3f}s - Error: {str(e)}"
                    )
                    raise
                
                # Calculate backoff delay (exponential backoff)
                delay = 2 ** attempt
                logger.warning(
                    f"HTTP {method} {full_url} failed (attempt {attempt + 1}/{self.max_retries + 1}) - "
                    f"Retrying in {delay}s - Error: {str(e)}"
                )
                time.sleep(delay)
    
    def get(self, url: str, params: Dict[str, Any] = None, headers: Dict[str, str] = None) -> requests.Response:
        """
        Make GET request.
        
        Args:
            url (str): Request URL
            params (Dict[str, Any]): Query parameters
            headers (Dict[str, str]): Additional headers
            
        Returns:
            requests.Response: HTTP response
        """
        return self._make_request('GET', url, params=params, headers=headers)
    
    def post(self, url: str, data: Dict[str, Any] = None, json: Dict[str, Any] = None, 
             headers: Dict[str, str] = None) -> requests.Response:
        """
        Make POST request.
        
        Args:
            url (str): Request URL
            data (Dict[str, Any]): Form data
            json (Dict[str, Any]): JSON data
            headers (Dict[str, str]): Additional headers
            
        Returns:
            requests.Response: HTTP response
        """
        return self._make_request('POST', url, data=data, json=json, headers=headers)
    
    def put(self, url: str, data: Dict[str, Any] = None, json: Dict[str, Any] = None,
            headers: Dict[str, str] = None) -> requests.Response:
        """
        Make PUT request.
        
        Args:
            url (str): Request URL
            data (Dict[str, Any]): Form data
            json (Dict[str, Any]): JSON data
            headers (Dict[str, str]): Additional headers
            
        Returns:
            requests.Response: HTTP response
        """
        return self._make_request('PUT', url, data=data, json=json, headers=headers)
    
    def patch(self, url: str, data: Dict[str, Any] = None, json: Dict[str, Any] = None,
              headers: Dict[str, str] = None) -> requests.Response:
        """
        Make PATCH request.
        
        Args:
            url (str): Request URL
            data (Dict[str, Any]): Form data
            json (Dict[str, Any]): JSON data
            headers (Dict[str, str]): Additional headers
            
        Returns:
            requests.Response: HTTP response
        """
        return self._make_request('PATCH', url, data=data, json=json, headers=headers)
    
    def delete(self, url: str, headers: Dict[str, str] = None) -> requests.Response:
        """
        Make DELETE request.
        
        Args:
            url (str): Request URL
            headers (Dict[str, str]): Additional headers
            
        Returns:
            requests.Response: HTTP response
        """
        return self._make_request('DELETE', url, headers=headers)
    
    def set_auth(self, auth: Union[tuple, requests.auth.AuthBase]) -> None:
        """
        Set authentication for all requests.
        
        Args:
            auth: Authentication object or tuple (username, password)
        """
        self.session.auth = auth
    
    def set_bearer_token(self, token: str) -> None:
        """
        Set Bearer token authentication.
        
        Args:
            token (str): Bearer token
        """
        self.session.headers.update({'Authorization': f'Bearer {token}'})
    
    def set_api_key(self, api_key: str, header_name: str = 'X-API-Key') -> None:
        """
        Set API key authentication.
        
        Args:
            api_key (str): API key
            header_name (str): Header name for API key
        """
        self.session.headers.update({header_name: api_key})
    
    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


class APIResponse:
    """Wrapper for API response with common utility methods."""
    
    def __init__(self, response: requests.Response):
        """
        Initialize API response wrapper.
        
        Args:
            response (requests.Response): HTTP response object
        """
        self.response = response
        self.status_code = response.status_code
        self.headers = response.headers
        self.url = response.url
    
    def json(self) -> Dict[str, Any]:
        """
        Get JSON response data.
        
        Returns:
            Dict[str, Any]: JSON response data
            
        Raises:
            ValueError: If response is not valid JSON
        """
        try:
            return self.response.json()
        except ValueError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            raise
    
    def text(self) -> str:
        """
        Get response text.
        
        Returns:
            str: Response text
        """
        return self.response.text
    
    def is_success(self) -> bool:
        """
        Check if response indicates success.
        
        Returns:
            bool: True if status code is 2xx, False otherwise
        """
        return 200 <= self.status_code < 300
    
    def is_client_error(self) -> bool:
        """
        Check if response indicates client error.
        
        Returns:
            bool: True if status code is 4xx, False otherwise
        """
        return 400 <= self.status_code < 500
    
    def is_server_error(self) -> bool:
        """
        Check if response indicates server error.
        
        Returns:
            bool: True if status code is 5xx, False otherwise
        """
        return 500 <= self.status_code < 600


def create_http_client(base_url: str = None, **kwargs) -> HTTPClient:
    """
    Factory function to create HTTP client instance.
    
    Args:
        base_url (str): Base URL for requests
        **kwargs: Additional client configuration
        
    Returns:
        HTTPClient: Configured HTTP client instance
    """
    return HTTPClient(base_url=base_url, **kwargs)
