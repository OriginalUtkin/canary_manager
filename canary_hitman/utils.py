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
def terminate_if_exception(exception_type: Type[HitmanException]) -> Generator:
    try:
        yield

    except exception_type as e:
        print(crayons.red(e.text))
        exit(1)

    except Exception:
        print(crayons.red("UnexpectedError"))

        raise
