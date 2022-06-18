from typing import Dict


class ImportException(Exception):

    def __init__(self, *args: object, errors: Dict[int, str]) -> None:
        super().__init__(*args)
        self.errors = errors
