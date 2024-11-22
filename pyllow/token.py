from typing import List, Dict, Optional, Any

from .request import make_request
from .config import logging


class Token:
    def __init__(
        self,
        token_endpoint: str,
        client_secret: str,
        refresh_token: str,
        client_id: str,
        access_token_path: List[str] = ["access_token"],
        refresh_token_path: List[str] = ["refresh_token"],
    ) -> None:
        """
        Initialize the Token class.

        Parameters
        ----------
        token_endpoint : str
            The endpoint URL to refresh the token.
        client_id : str
            The client ID for authentication.
        client_secret : str
            The client secret for authentication.
        refresh_token : str
            The refresh token value.
        access_token_path : List[str], optional
            The JSON path to extract the access token from the response.
        refresh_token_path : List[str], optional
            The JSON path to extract the refresh token from the response.
        """
        self.token_endpoint = token_endpoint
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.access_token = ""
        self.access_token_path = access_token_path
        self.refresh_token_path = refresh_token_path

    def refresh_access_token(self, headers: Dict[str, str]) -> str:
        """
        Refresh the access token using the refresh token.

        Parameters
        ----------
        headers : Dict[str, str]
            The headers to include in the token refresh request.

        Returns
        -------
        str
            The new access token.
        """
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        try:
            response = make_request(
                method="POST",
                url=self.token_endpoint,
                headers=headers,
                data=payload,
                verify_ssl=True,
            )
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = self._extract_value(
                    token_data, self.access_token_path
                )
                new_refresh_token = self._extract_value(
                    token_data, self.refresh_token_path
                )
                if new_refresh_token:
                    self.refresh_token = new_refresh_token
                return self.access_token
            else:
                logging.error(
                    f"Token refresh failed with status code {response.status_code}"
                )
                raise Exception("Token refresh failed")
        except Exception as e:
            logging.error(f"Error refreshing token: {e}")
            raise

    @staticmethod
    def _extract_value(data: Dict[str, Any], path: List[str]) -> Optional[str]:
        """
        Extract a value from a nested dictionary given a path.

        Parameters
        ----------
        data : Dict[str, Any]
            The JSON data to extract the value from.
        path : List[str]
            The list of keys representing the path to the desired value.

        Returns
        -------
        Optional[str]
            The extracted value or None if not found.
        """
        for key in path:
            if isinstance(data, dict):
                data = data.get(key)
            else:
                return None
        if isinstance(data, str):
            return data
        return None
