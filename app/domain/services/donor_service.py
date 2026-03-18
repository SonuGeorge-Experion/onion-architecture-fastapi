from app.domain.exceptions import DuplicateZNumberException


class DonorService:

    async def validate_unique_znumber(self, znumber, repository):

        existing = await repository.exists_by_znumber(znumber)

        if existing:
            raise DuplicateZNumberException(znumber)
