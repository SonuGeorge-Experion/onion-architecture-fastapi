from injector import Injector

from app.container.module.repository_module import RepositoryModule
from app.core.singleton import Singleton


class DIContainer(Singleton):
    MODULES = [RepositoryModule]
    injector: Injector = Injector(MODULES)

    def resolve(self, cls: object) -> object:
        return self.injector.get(cls)
