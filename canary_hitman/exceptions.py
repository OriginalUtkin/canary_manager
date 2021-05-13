class HitmanException(Exception):
    text = "Base hitman exception class text"


class MissingVariableException(HitmanException):
    def __init__(self, variable_name: str) -> None:
        self.text = f"Variable {variable_name} is missing in environment"
