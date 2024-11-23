# Pyllow
![First mention of Pyllow](https://i.postimg.cc/WbfgxVRC/DALL-E-2024-11-23-12-21-20-An-ancient-cave-painting-style-depiction-of-a-laptop-as-a-creature-fea.webp)

## Introduction

**Pyllow** is a Python library designed to simulate mass HTTP requests for testing and benchmarking purposes. It provides a flexible and powerful interface to perform large-scale request simulations, handle token authentication with automatic refresh, process responses based on custom conditions, and manage output logging with file handling options.

Whether you are testing API endpoints, performing stress tests, or automating request sequences, Pyllow simplifies the process by abstracting the complexities involved in making HTTP requests at scale.

## Features

- **Mass Request Simulation**: Send a large number of HTTP requests (GET, POST, etc.) with customizable payloads and parameters.
- **Token Management**: Automatically handle token authentication, including refreshing access tokens using refresh tokens when they expire.
- **Conditional Response Handling**: Define custom conditions to filter and save responses based on status codes or specific messages in the response content.
- **Looping Mechanism**: Repeat requests multiple times using the loops feature, which is especially useful for stress testing.
- **Advanced Logging and Output Management**:
  - Save all responses to an output file.
  - Append results to existing files instead of overwriting them.
  - Maintain progress logs to monitor the execution between 0% and 100%.
- **Configurable Delays**: Introduce sleep intervals between requests to control the request rate.
- **SSL Verification Control**: Enable or disable SSL verification for requests.

## Installation

Pyllow can be installed via `pip`. (Note: If Pyllow is not yet available on PyPI, you can clone it from the repository and install it manually.)

```bash
pip install pyllow
```

## Usage Examples

Below are examples demonstrating how to use Pyllow for different scenarios.

### Example 1: Basic Mass GET Requests

```python
from pyllow import Pyllow

# Define the headers for the requests
headers = {
    "Accept": "application/json"
}

# Initialize the Pyllow for GET requests
simulator = Pyllow(
    method="GET",
    url="https://api.example.com/data",
    headers=headers,
    loops=10,               # Repeat the GET request 10 times
    sleep_time=1,           # Sleep for 1 second between requests
    verify_ssl=True,        # Enable SSL verification
    save_output=True,       # Save all responses to a file
    output_file="responses.txt",
    append_logs=False       # Overwrite the output file if it exists
)

# Run the simulation
simulator.run()
```

**Explanation:**

- Sends a GET request to the specified URL 10 times.
- Sleeps for 1 second between each request.
- Saves all responses to `responses.txt`, overwriting the file if it exists.

### Example 2: Mass POST Requests with Payloads and Token Authentication

```python
from pyllow import Pyllow, Token

# Initialize the token for authentication
token = Token(
    token_endpoint="https://api.example.com/oauth/token",
    client_id="your_client_id",
    client_secret="your_client_secret",
    refresh_token="initial_refresh_token",
    access_token_path=["access_token"],
    refresh_token_path=["refresh_token"]
)

# Define the headers for the requests
headers = {
    "Content-Type": "application/json"
}

# Define a list of payloads for POST requests
payloads = [
    {"user_id": 1, "action": "login"},
    {"user_id": 2, "action": "login"},
    {"user_id": 3, "action": "login"},
    # Add more payloads as needed
]

# Initialize the Pyllow for POST requests with payloads
simulator = Pyllow(
    method="POST",
    url="https://api.example.com/user/actions",
    headers=headers,
    payloads=payloads,
    token=token,            # Use token authentication
    loops=5,                # Repeat the payloads 5 times
    sleep_time=0.5,         # Sleep for 0.5 seconds between requests
    verify_ssl=True,
    save_output=True,
    output_file="all_responses.txt",
    append_logs=True        # Append to the output file if it exists
)

# Run the simulation
simulator.run()
```

**Explanation:**

- Sends POST requests to the specified URL with each payload in the list.
- Repeats the entire payload list 5 times due to the `loops` parameter.
- Uses the `Token` class to handle authentication, including automatic token refreshing.
- Sleeps for 0.5 seconds between each request.
- Saves all responses to `all_responses.txt`, appending to the file if it exists.

### Example 3: Conditional Response Handling

```python
from pyllow import Pyllow

# Define the headers for the requests
headers = {
    "Accept": "application/json"
}

# Define conditions to save responses based on status codes and messages
conditions = [
    {
        "status_codes": [200],
        "messages": ["success"],
        "output_file": "success_responses.txt"
    },
    {
        "status_codes": [400, 404],
        "messages": ["error", "not found"],
        "output_file": "error_responses.txt"
    }
]

# Initialize the Pyllow with conditions
simulator = Pyllow(
    method="GET",
    url="https://api.example.com/data",
    headers=headers,
    loops=20,
    sleep_time=0.2,
    verify_ssl=True,
    conditions=conditions,
    append_logs=True        # Append to the condition output files if they exist
)

# Run the simulation
simulator.run()
```

**Explanation:**

- Sends a GET request 20 times.
- Checks each response against the specified conditions:
  - If the response has a status code of 200 and contains the word "success", it is saved to `success_responses.txt`.
  - If the response has a status code of 400 or 404 and contains "error" or "not found", it is saved to `error_responses.txt`.
- Appends results to the condition output files if they exist.

### Example 4: Disabling SSL Verification and Custom Sleep Time

```python
from pyllow import Pyllow

# Define the headers for the requests
headers = {
    "Accept": "application/json"
}

# Initialize the Pyllow with SSL verification disabled
simulator = Pyllow(
    method="GET",
    url="https://api.example.com/insecure",
    headers=headers,
    loops=5,
    sleep_time=2,           # Sleep for 2 seconds between requests
    verify_ssl=False,       # Disable SSL verification
    save_output=True,
    output_file="insecure_responses.txt",
    append_logs=False
)

# Run the simulation
simulator.run()
```

**Explanation:**

- Sends a GET request to an endpoint with a self-signed or invalid SSL certificate.
- Disables SSL verification using `verify_ssl=False`.
- Sleeps for 2 seconds between requests.
- Saves all responses to `insecure_responses.txt`, overwriting the file if it exists.

## Classes and Methods

### `Pyllow` Class

#### Constructor Parameters

- **method** (`str`): The HTTP method to use (e.g., `"GET"`, `"POST"`).
- **url** (`str`): The URL to send requests to.
- **headers** (`Dict[str, str]`): Headers to include in each request.
- **payloads** (`Optional[List[Dict[str, Any]]]`, optional): A list of payloads for `POST` requests.
- **params** (`Optional[Dict[str, Any]]`, optional): Query parameters for `GET` requests.
- **token** (`Optional[Token]`, optional): An instance of the `Token` class for token management.
- **save_output** (`bool`, optional): Whether to save all responses to an output file.
- **output_file** (`str`, optional): The file path to save all responses.
- **conditions** (`Optional[List[Dict[str, Any]]]`, optional): A list of conditions to save responses based on status code or message.
- **sleep_time** (`float`, optional): The time to sleep between requests in seconds.
- **verify_ssl** (`bool`, optional): Whether to verify SSL certificates.
- **loops** (`int`, optional): The number of times to repeat the requests.
- **append_logs** (`bool`, optional): If `True`, append results to existing files instead of overwriting.

#### Methods

- **run()**: Executes the mass request simulation.
- **_make_request(payload)**: Makes a single HTTP request (internal use).
- **_process_response(response)**: Processes the HTTP response (internal use).
- **_log_progress()**: Logs the progress of the mass requests (internal use).
- **_save_results()**: Saves all responses to the output file (internal use).
- **_save_condition_results()**: Saves responses that matched conditions to their respective output files (internal use).

### `Token` Class

#### Constructor Parameters

- **token_endpoint** (`str`): The endpoint URL to refresh the token.
- **client_id** (`str`): The client ID for authentication.
- **client_secret** (`str`): The client secret for authentication.
- **refresh_token** (`str`): The refresh token value.
- **access_token_path** (`List[str]`, optional): The JSON path to extract the access token from the response.
- **refresh_token_path** (`List[str]`, optional): The JSON path to extract the refresh token from the response.

#### Methods

- **refresh_access_token(headers)**: Refreshes the access token using the refresh token.
- **_extract_value(data, path)**: Extracts a value from a nested dictionary given a path (internal use).

### `request` Function

A utility function to make an HTTP request.

#### Parameters

- **method** (`str`): The HTTP method to use.
- **url** (`str`): The URL to send the request to.
- **headers** (`Dict[str, str]`): Headers to include in the request.
- **data** (`Optional[Dict[str, Any]]`, optional): Payload for `POST` requests.
- **params** (`Optional[Dict[str, Any]]`, optional): Query parameters for `GET` requests.
- **verify_ssl** (`bool`, optional): Whether to verify SSL certificates.

#### Returns

- **requests.Response**: The HTTP response object.

### Customizing Token Refresh Logic

If the token response structure is different, you can adjust the `access_token_path` and `refresh_token_path` when initializing the `Token` class.

**Example:**

```python
token = Token(
    token_endpoint="https://api.example.com/oauth/token",
    client_id="your_client_id",
    client_secret="your_client_secret",
    refresh_token="initial_refresh_token",
    access_token_path=["data", "accessToken"],
    refresh_token_path=["data", "refreshToken"]
)
```

## Extending Pyllow

Since Pyllow is built with clean code principles, it's straightforward to extend or customize its functionality.

- **Add Custom Request Methods**: Extend the `Pyllow` class to handle additional HTTP methods or protocols.
- **Implement Additional Authentication Schemes**: Modify or subclass the `Token` class to support other authentication mechanisms.
- **Enhance Response Processing**: Override the `_process_response` method to include additional processing logic.

## Conclusion

Pyllow simplifies the process of simulating mass HTTP requests for testing and development purposes. With its robust feature set and flexible architecture, you can tailor it to fit a wide range of scenarios.

Whether you need to perform stress tests, automate API interactions, or process responses based on complex conditions, Pyllow provides the tools to get the job done efficiently.

## Repository and Contributions

Pyllow is open-source and welcomes contributions from the community. You can find the source code and contribute on GitHub:

[GitHub Repository](https://github.com/MuriloCarlos1567/pyllow/)

## License

Pyllow is licensed under the MIT License.

## Contact and Support

For questions, issues, or feature requests, please open an issue on the GitHub repository or contact the maintainer at:

- **Email**: efgs96@gmail.com
- **GitHub Issues**: [GitHub Issues](https://github.com/MuriloCarlos1567/pyllow/issues)

Happy testing with Pyllow!