from dataclasses import dataclass


@dataclass(frozen=True)
class Quotation:
    name: str
    kind: str
    price: int

    def __post_init__(self):
        if not isinstance(self.price, int) or self.price <= 0:
            raise ValueError(
                "Preço deve ser um inteiro não negativo e diferente de zero.",
            )
        if not self.name or not self.kind:
            raise ValueError("Nome e sigla não podem ser vazios")
