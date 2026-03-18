from app.domain.exceptions import DuplicateZNumberException


class DonorService:

    def validate_unique_znumber(self, znumber, repository):

        existing = repository.exists_by_znumber(znumber)

        if existing:
            raise DuplicateZNumberException("ZNumber already exists")
