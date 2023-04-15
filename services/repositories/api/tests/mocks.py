import json


class MockClientResponse:
    def __init__(self, text, status):
        self._text = text
        self.status = status

    async def read(self):
        return self._text

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self

    async def json(self):
        return json.loads(self._text)
