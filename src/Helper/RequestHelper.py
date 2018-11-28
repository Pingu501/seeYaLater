from urllib.parse import urlencode
from urllib.request import Request, urlopen

import json
import logging

logger = logging.getLogger()


def synchronousApiRequest(url, post_fields):
    request = Request(url, urlencode(post_fields).encode())

    try:
        response = urlopen(request).read().decode()
    except Exception:
        logger.error("could not connect to the API")
        return None

    return json.loads(response)
