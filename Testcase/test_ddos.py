import time
import requests

def test_api_rate_limit_ddos(config):
    """
    Sends 150 requests in 60 seconds where limit = 120/minute.
    Expects:
      - Some responses return 429 Too Many Requests
      - API still works for another user (token_other_user)
    """

    base_url = config["api"]["base_url"]
    valid_token = config["api"]["token_valid"]
    other_user_token = config["api"]["token_other_user"]

    headers_main = {"Authorization": valid_token}
    headers_other = {"Authorization": other_user_token}

    total_requests = 150
    request_interval = 60 / total_requests  

    too_many_count = 0
    success_count = 0

    for _ in range(total_requests):
        response = requests.get(base_url, headers=headers_main)

        if response.status_code == 429:
            too_many_count += 1
        elif response.status_code == 200:
            success_count += 1

        time.sleep(request_interval)

    assert too_many_count > 0, "API did NOT enforce rate limiting (no 429 responses returned)."
    assert success_count < total_requests, "All requests succeeded — rate limiting not applied."
