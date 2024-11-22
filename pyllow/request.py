from typing import Dict, Optional, Any
import requests
import logging


def make_request(
    method: str,
    url: str,
    headers: Dict[str, str],
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    verify_ssl: bool = True,
) -> requests.Response:
    """
    Make an HTTP request.

    Parameters
    ----------
    method : str
        The HTTP method ('GET', 'POST', etc.).
    url : str
        The URL to send the request to.
    headers : Dict[str, str]
        The headers to include in the request.
    data : Optional[Dict[str, Any]], optional
        The payload for POST requests.
    params : Optional[Dict[str, Any]], optional
        The query parameters for GET requests.
    verify_ssl : bool, optional
        Whether to verify SSL certificates.

    Returns
    -------
    requests.Response
        The HTTP response.
    """
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            params=params,
            verify=verify_ssl,
        )
        return response
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        raise
