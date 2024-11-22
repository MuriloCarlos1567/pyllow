from typing import List, Dict, Optional, Any
import requests
import time
import os

from .request import make_request
from .config import logging
from .token import Token


class Pyllow:
    def __init__(
        self,
        method: str,
        url: str,
        headers: Dict[str, str],
        payloads: Optional[List[Dict[str, Any]]] = None,
        params: Optional[Dict[str, Any]] = None,
        token: Optional[Token] = None,
        save_output: bool = False,
        output_file: str = "output.txt",
        conditions: Optional[List[Dict[str, Any]]] = None,
        sleep_time: float = 0,
        verify_ssl: bool = True,
        loops: int = 1,
        append_logs: bool = False,
    ) -> None:
        """
        Initialize the Pyllow.

        Parameters
        ----------
        method : str
            The HTTP method ('GET', 'POST', etc.).
        url : str
            The URL to send requests to.
        headers : Dict[str, str]
            The headers to include in the requests.
        payloads : Optional[List[Dict[str, Any]]], optional
            A list of payloads for POST requests.
        params : Optional[Dict[str, Any]], optional
            The query parameters for GET requests.
        token : Optional[Token], optional
            An instance of the Token class for token management.
        save_output : bool, optional
            Whether to save all responses to an output file.
        output_file : str, optional
            The file path to save all responses.
        conditions : Optional[List[Dict[str, Any]]], optional
            A list of conditions to save responses based on status code or message.
            Each condition is a dictionary with keys:
            - 'status_codes': Optional[List[int]]
            - 'messages': Optional[List[str]]
            - 'output_file': str
        sleep_time : float, optional
            The time to sleep between requests in seconds.
        verify_ssl : bool, optional
            Whether to verify SSL certificates.
        loops : int, optional
            The number of times to repeat the requests.
        append_logs : bool, optional
            If True, append results to existing files instead of overwriting.
        """
        self.method = method
        self.url = url
        self.headers = headers
        self.payloads = payloads or [{}]
        self.params = params
        self.token = token
        self.save_output = save_output
        self.output_file = output_file
        self.conditions = conditions or []
        self.sleep_time = sleep_time
        self.verify_ssl = verify_ssl
        self.loops = loops
        self.append_logs = append_logs
        self.results: List[str] = []
        self.total_requests = (
            len(self.payloads) * self.loops
            if self.method.upper() == "POST"
            else self.loops
        )
        self.completed_requests = 0
        self.condition_results: List[Dict[str, Any]] = []

        for condition in self.conditions:
            self.condition_results.append({"condition": condition, "results": []})

    def run(self) -> None:
        """
        Execute the mass request simulation.
        """
        for _ in range(self.loops):
            if self.method.upper() == "POST":
                for payload in self.payloads:
                    self._make_request(payload)
                    self.completed_requests += 1
                    self._log_progress()
                    if self.sleep_time > 0:
                        time.sleep(self.sleep_time)
            else:
                self._make_request({})
                self.completed_requests += 1
                self._log_progress()
                if self.sleep_time > 0:
                    time.sleep(self.sleep_time)

        if self.save_output:
            self._save_results()

        self._save_condition_results()

    def _make_request(self, payload: Dict[str, Any]) -> None:
        """
        Make a single HTTP request.

        Parameters
        ----------
        payload : Dict[str, Any]
            The payload for the request.
        """
        try:
            if self.token and self.token.access_token:
                self.headers["Authorization"] = f"Bearer {self.token.access_token}"

            response = make_request(
                method=self.method,
                url=self.url,
                headers=self.headers,
                data=payload if self.method.upper() == "POST" else None,
                params=self.params if self.method.upper() == "GET" else None,
                verify_ssl=self.verify_ssl,
            )

            if response.status_code == 401 and self.token:
                self.token.refresh_access_token(self.headers)
                self.headers["Authorization"] = f"Bearer {self.token.access_token}"
                response = make_request(
                    method=self.method,
                    url=self.url,
                    headers=self.headers,
                    data=payload if self.method.upper() == "POST" else None,
                    params=self.params if self.method.upper() == "GET" else None,
                    verify_ssl=self.verify_ssl,
                )

            self._process_response(response)
        except Exception as e:
            logging.error(f"Error during request: {e}")

    def _process_response(self, response: requests.Response) -> None:
        """
        Process the HTTP response.

        Parameters
        ----------
        response : requests.Response
            The HTTP response to process.
        """
        content = response.text

        if self.save_output:
            self.results.append(content)

        for condition_result in self.condition_results:
            condition = condition_result["condition"]
            match = True

            if "status_codes" in condition and condition["status_codes"]:
                if response.status_code not in condition["status_codes"]:
                    match = False

            if "messages" in condition and condition["messages"]:
                if not any(message in content for message in condition["messages"]):
                    match = False

            if match:
                condition_result["results"].append(content)

    def _log_progress(self) -> None:
        """
        Log the progress of the mass requests.
        """
        progress = (self.completed_requests / self.total_requests) * 100
        logging.info(f"Progress: {progress:.2f}%")

    def _save_results(self) -> None:
        """
        Save all responses to the output file.
        """
        mode = "a" if self.append_logs and os.path.exists(self.output_file) else "w"
        try:
            with open(self.output_file, mode, encoding="utf-8") as file:
                for result in self.results:
                    file.write(result + "\n")
            logging.info(f"All results saved to {self.output_file}")
        except IOError as e:
            logging.error(f"Error saving results: {e}")

    def _save_condition_results(self) -> None:
        """
        Save responses that matched conditions to their respective output files.
        """
        for condition_result in self.condition_results:
            condition = condition_result["condition"]
            output_file = condition.get("output_file")
            results = condition_result["results"]
            if output_file and results:
                mode = "a" if self.append_logs and os.path.exists(output_file) else "w"
                try:
                    with open(output_file, mode, encoding="utf-8") as file:
                        for result in results:
                            file.write(result + "\n")
                    logging.info(f"Results for condition saved to {output_file}")
                except IOError as e:
                    logging.error(
                        f"Error saving condition results to {output_file}: {e}"
                    )
