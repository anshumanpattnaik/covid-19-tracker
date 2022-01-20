from typing import Generic, TypeVar

T = TypeVar('T')


class Response(Generic[T]):
    def __init__(self, response, cls: T = None):
        self.response = response
        self.cls = cls

    def status_code(self):
        return self.response.status_code

    def obj(self) -> T:
        return self.cls.object(self.response.json())
