from app.domain.exceptions import InvalidZNumberException


class ZNumber:

    def __init__(self, value: int):

        # if not value.startswith("Z"):
        #     raise InvalidZNumberException("Invalid ZNumber format. Must start with 'Z'.")

        if len(str(value)) != 5:
            raise InvalidZNumberException("ZNumber must be length 5")

        self.value = value

    def __int__(self):
        return self.value
