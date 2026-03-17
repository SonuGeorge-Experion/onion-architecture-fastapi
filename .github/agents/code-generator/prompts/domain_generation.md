# Domain Generation Prompt

Generate domain entities and domain services.

Rules:

- use Python dataclasses
- avoid framework imports
- contain business rules
- maintain immutability where appropriate

Example entity:

@dataclass
class Donor:
    donor_id: Optional[int]
    znumber: int
    name: str