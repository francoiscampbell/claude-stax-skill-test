from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    username: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

    def display_name(self) -> str:
        return f"{self.username} <{self.email}>"

    def deactivate(self) -> None:
        self.is_active = False
