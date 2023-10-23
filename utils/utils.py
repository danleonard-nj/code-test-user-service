import logging


# Sample in-memory database of fake users
USERS_DB = {
    1: {"user_id": 1, "friends": [2, 3]},
    2: {"user_id": 2, "friends": [3]},
    3: {"user_id": 3, "friends": []},
}


def get_console_handler():
    console = logging.StreamHandler()
    formatter = logging.Formatter(
        '[%(asctime)-8s] [%(thread)-4s] [%(name)-12s]: [%(levelname)-4s]: %(message)s')
    console.setFormatter(formatter)
    return console


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_console_handler())
    return logger


class ArgumentNullException(Exception):
    def __init__(self, arg_name, *args: object) -> None:
        super().__init__(f"Argument '{arg_name}' cannot be null")

    @staticmethod
    def if_none(value, arg_name):
        if value is None:
            raise ArgumentNullException(arg_name)

    @staticmethod
    def if_none_or_whitespace(value, arg_name):
        if value is None or value == '':
            raise ArgumentNullException(arg_name)

    @staticmethod
    def if_none_or_empty(value, arg_name):
        if not any(value):
            raise ArgumentNullException(arg_name)
