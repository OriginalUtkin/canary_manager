import os


def get_environ_var(variable_name: str) -> str:
    variable_val = os.getenv(variable_name)

    if not variable_val:
        raise Exception

    return variable_val
