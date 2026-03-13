class DomainException(Exception):
    """Base class for all domain exceptions"""

    pass


class DuplicateZNumberException(DomainException):
    def __init__(self, znumber: str):
        self.message = f"Donor with Z-number {znumber} already exists."
        super().__init__(self.message)


class InvalidZNumberException(DomainException):
    def __init__(self, message: str = "Invalid ZNumber"):
        super().__init__(message)
