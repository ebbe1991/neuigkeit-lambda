import json


class HttpException(Exception):
    def __init__(self,
                 error_text: str,
                 http_status: int):
        self.error_text = error_text
        self.http_status = http_status

    def to_json(self):
        return json.dumps({
            "error_text": self.error_text,
        })


class ValidationException(HttpException):
    def __init__(self, reason: str):
        super().__init__(http_status=400,
                         error_text=reason)
