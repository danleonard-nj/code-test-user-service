

class Serializable:
    def to_dict(self):
        return self.__dict__


class ErrorResponse(Serializable):
    def __init__(
        self,
        error_type: str,
        message: str
    ):
        self.error_type = error_type
        self.message = message
