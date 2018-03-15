from urllib.parse import urlencode
from urllib.request import Request, urlopen

import json

from src.Helper import Logger


def synchronousApiRequest(url, post_fields):
    request = Request(url, urlencode(post_fields).encode())

    try:
        response = urlopen(request).read().decode()
    except Exception:
        Logger.createLogEntry("could not connect to the API")
        return None

    return json.loads(response)
