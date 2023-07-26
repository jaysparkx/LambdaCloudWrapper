def process_request(request_obj):
    if 200 <= request_obj.status_code <= 299:
        return request_obj.json()
    return request_obj.raise_for_status()
