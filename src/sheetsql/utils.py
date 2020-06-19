import json

import regex
from requests import Response

from .exceptions import InvalidQueryException

EXTRACT_JSON_REGEX = regex.compile(r"\{(?:[^{}]|(?R))*\}")
TQ_BASE_URL = "https://spreadsheets.google.com/tq"


def parse_json_from_tq_response(response_text: str) -> dict:
    return json.loads(EXTRACT_JSON_REGEX.findall(response_text)[0])


def handle_tq_response(response: Response) -> dict:
    response_json = parse_json_from_tq_response(response.text)
    if response_json["status"] == "error":
        raise InvalidQueryException(
            f"Response went through but received invalid query {response_json}"
        )
    return response_json["table"]
