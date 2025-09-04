# utils/api_helpers.py

import requests
import time
import logging
from API.utils.settings import BASE_URL

RETRIES = 30  # Max retry attempts
DELAY = 1  # Delay between retries in seconds
DEFAULT_TIMEOUT = 20  # Request timeout in seconds
RETRY_STATUS_CODES = {500}  # Only retry on these status codes

logger = logging.getLogger("qa_tests")


def api_request(method, path, **kwargs):
    """
    Make an HTTP request with retry logic for specific errors.
    Returns Response on success; raises Exception on final 5xx/timeout.
    """
    url = f"{BASE_URL}{path}"
    last_exc = None
    failed_attempts = 0

    for attempt in range(RETRIES):
        try:
            r = requests.request(method, url, timeout=DEFAULT_TIMEOUT, **kwargs)

            if 500 <= r.status_code <= 599 and r.status_code not in RETRY_STATUS_CODES:
                raise Exception(f"Server error {r.status_code} for {url}\nBody: {r.text[:500]}...")

            if r.status_code not in RETRY_STATUS_CODES:
                if failed_attempts > 0:
                    logger.info(f"api_request succeeded after {failed_attempts} retries")
                return r

            failed_attempts += 1
            if attempt == RETRIES - 1:
                logger.error(
                    f"Final attempt failed after {failed_attempts} retries\n"
                    f"URL: {url}\nStatus: {r.status_code}\n"
                    f"Response: {r.text[:500]}..."
                )

        except requests.exceptions.ReadTimeout as e:
            failed_attempts += 1
            last_exc = e
        except Exception as e:
            logger.error(f"Non-retryable error: {str(e)}")
            raise

        time.sleep(DELAY)

    if last_exc:
        raise last_exc
    raise Exception(f"Request failed after {RETRIES} retries (Last status: 500)")
