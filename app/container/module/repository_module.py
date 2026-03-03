# from app.domain.repositories.donor_repository import DonorRepository
from injector import Binder, Module

# from app.infrastructure.db.repositories.donor_repository import (
#     DonorRepositoryORM,
# )


class RepositoryModule(Module):
    def configure(self, binder: Binder) -> None:
        # binder.bind(DonorRepository, to=DonorRepositoryORM)
        pass
