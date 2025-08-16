# utils/api_helpers.py

import requests
import time
import logging
from utils.settings import BASE_URL

RETRIES = 15  # Max retry attempts
DELAY = 1  # Delay between retries in seconds
DEFAULT_TIMEOUT = 20  # Request timeout in seconds
RETRY_STATUS_CODES = {500}  # Only retry on these status codes

logger = logging.getLogger("qa_tests")


def api_request(method, path, **kwargs):
    """Make an HTTP request with retry logic for specific errors.

    Args:
        method: HTTP method (GET, POST, etc.)
        path: API endpoint path
        **kwargs: Additional arguments for requests.request

    Returns:
        requests.Response: Successful response

    Raises:
        Exception: If all retries fail or non-retryable error occurs
    """
    url = f"{BASE_URL}{path}"
    last_exc = None
    failed_attempts = 0

    for attempt in range(RETRIES):
        try:
            # Make the HTTP request
            r = requests.request(method, url, timeout=DEFAULT_TIMEOUT, **kwargs)

            # Success case or non-retryable error
            if r.status_code not in RETRY_STATUS_CODES:
                if failed_attempts > 0:
                    logger.info(f"Request succeeded after {failed_attempts} retries")
                return r

            # Only retry for status codes in RETRY_STATUS_CODES (500)
            failed_attempts += 1
            if attempt == RETRIES - 1:  # Final attempt failed
                logger.error(
                    f"Final attempt failed after {failed_attempts} retries\n"
                    f"URL: {url}\nStatus: {r.status_code}\n"
                    f"Response: {r.text[:500]}..."
                )

        except requests.exceptions.ReadTimeout as e:
            # Network timeout - considered retryable
            failed_attempts += 1
            last_exc = e
        except Exception as e:
            # Non-retryable errors (connection, SSL, etc.)
            logger.error(f"Non-retryable error: {str(e)}")
            raise  # Immediate failure

        time.sleep(DELAY)

    # All retries exhausted
    if last_exc:
        raise last_exc
    raise Exception(f"Request failed after {RETRIES} retries (Last status: 500)")