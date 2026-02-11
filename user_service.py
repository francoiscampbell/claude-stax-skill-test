from dataclasses import dataclass, field
from datetime import datetime

USERNAME_MIN_LENGTH = 3


class ValidationError(Exception):
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        super().__init__(f"{field}: {message}")


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

    def validate_username(self) -> None:
        if len(self.username) < USERNAME_MIN_LENGTH:
            raise ValidationError(
                "username",
                f"must be at least {USERNAME_MIN_LENGTH} characters",
            )
        if not self.username.isalnum():
            raise ValidationError("username", "must be alphanumeric")

    def validate(self) -> None:
        self.validate_username()
