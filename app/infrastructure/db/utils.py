import inspect
from dataclasses import asdict
from dataclasses import is_dataclass
from dataclasses import is_dataclass as _is_dataclass
from typing import Any, Dict, Type


def prepare_model_payload(
    domain_obj: Any, id_field: str = "donor_id"
) -> Dict[str, Any]:
    """Return a dict suitable for model construction by removing the id field.

    Accepts dataclasses or objects with `__dict__`.
    """
    if is_dataclass(domain_obj):
        payload = asdict(domain_obj)
    else:
        payload = dict(getattr(domain_obj, "__dict__", {}) or {})

    payload.pop(id_field, None)
    return payload


def model_to_domain(model: Any, domain_cls: Type[Any]) -> Any:
    """Create a domain dataclass/obj from a SQLAlchemy model instance.

    Extracts column values from `model.__table__.columns` and passes them
    into `domain_cls` as keyword arguments.
    """
    values = {c.name: getattr(model, c.name) for c in model.__table__.columns}

    # Determine which keyword names the domain class accepts and filter values.
    allowed_keys = None
    if _is_dataclass(domain_cls):
        allowed_keys = set(domain_cls.__dataclass_fields__.keys())
    else:
        try:
            sig = inspect.signature(domain_cls)
            # Exclude 'self' and var-keyword
            allowed_keys = set(
                name
                for name, param in sig.parameters.items()
                if name != "self"
                and param.kind in (param.POSITIONAL_OR_KEYWORD, param.KEYWORD_ONLY)
            )
        except (TypeError, ValueError):
            allowed_keys = None

    if allowed_keys is not None:
        filtered = {k: v for k, v in values.items() if k in allowed_keys}
    else:
        filtered = values

    return domain_cls(**filtered)
