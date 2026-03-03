class DomainException(Exception):
    """Base class for all domain exceptions"""

    pass


class DuplicateZNumberException(DomainException):
    def __init__(self, znumber: str):
        self.message = f"Donor with Z-number {znumber} already exists."
        super().__init__(self.message)
