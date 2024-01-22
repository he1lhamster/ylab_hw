from dataclasses import dataclass


@dataclass
class MenuSchema:
    title: str
    description: str


@dataclass
class SubmenuSchema:
    title: str
    description: str


@dataclass
class DishSchema:
    title: str
    description: str
    price: str
