import hashlib
import secrets
from dataclasses import dataclass, field
from datetime import datetime

USERNAME_MIN_LENGTH = 3


class ValidationError(Exception):
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        super().__init__(f"{field}: {message}")


class AuthenticationError(Exception):
    pass


@dataclass
class User:
    username: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    password_hash: str = ""
    auth_token: str = ""

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

    def set_password(self, password: str) -> None:
        self.validate()  # ensure user is valid before setting credentials
        salt = secrets.token_hex(16)
        self.password_hash = salt + ":" + hashlib.sha256(
            (salt + password).encode()
        ).hexdigest()

    def check_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        salt, expected = self.password_hash.split(":", 1)
        actual = hashlib.sha256((salt + password).encode()).hexdigest()
        return secrets.compare_digest(actual, expected)

    def authenticate(self, password: str) -> str:
        if not self.is_active:
            raise AuthenticationError("account is deactivated")
        try:
            self.validate()
        except ValidationError as e:
            raise AuthenticationError(f"invalid user: {e}") from e
        if not self.check_password(password):
            raise AuthenticationError("incorrect password")
        self.auth_token = secrets.token_urlsafe(32)
        return self.auth_token
