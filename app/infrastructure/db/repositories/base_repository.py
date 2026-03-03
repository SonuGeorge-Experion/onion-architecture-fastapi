from typing import Any, Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.utils import model_to_domain, prepare_model_payload


class BaseRepository:
    """Generic base repository providing create functionality.

    Subclasses should set `model_cls` (SQLAlchemy model) and `domain_cls`
    (domain dataclass/class) or pass them to the constructor.
    """

    def __init__(
        self, session: AsyncSession, model_cls: Type[Any], domain_cls: Type[Any]
    ):
        self.session = session
        self.model_cls = model_cls
        self.domain_cls = domain_cls

    async def create(self, domain_obj: Any, id_field: str = "id") -> Any:
        payload = prepare_model_payload(domain_obj, id_field=id_field)
        model = self.model_cls(**payload)

        async with self.session.begin():
            self.session.add(model)
            await self.session.flush()

        await self.session.refresh(model)
        return model_to_domain(model, self.domain_cls)
