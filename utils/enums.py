from enum import Enum

class Register(Enum):
    USERNAME_MIN_LENGTH = 4
    USERNAME_MAX_LENGTH = 32
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_MAX_LENGTH = 128


def GET_ENUM(enum_value):
    return (enum_value)
