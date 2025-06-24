from dataclasses import dataclass


@dataclass(frozen=True)
class Quotation:
    name: str
    kind: str
    price: int

    def __post_init__(self):
        if not isinstance(self.price, int) or self.price <= 0:
            raise ValueError(
                "Price must be a non-negative integer and not equal to zero.",
            )
        if not self.name or not self.kind:
            raise ValueError("Name and kind cannot be empty")
