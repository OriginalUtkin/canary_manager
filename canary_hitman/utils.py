import os
from contextlib import contextmanager
from typing import Generator, Type

import crayons

from .exceptions import HitmanException, MissingVariableException


def get_environ_var(variable_name: str) -> str:
    variable_val = os.getenv(variable_name)

    if not variable_val:
        raise MissingVariableException(variable_name=variable_name)

    return variable_val


@contextmanager
def handle_exception(custom_exception: Type[HitmanException]) -> Generator:
    try:
        yield

    except custom_exception as e:
        print(crayons.red(e.text))
        exit(1)

    except Exception:
        print(crayons.red("UnexpectedError"))
