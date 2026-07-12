from __future__ import annotations

from contextlib import suppress
from dataclasses import dataclass, field

import keyring
from keyring.errors import KeyringError

SERVICE = "CleanText Studio"


@dataclass(slots=True)
class CredentialStore:
    session: dict[str, str] = field(default_factory=dict)

    def save(self, config_name: str, key: str, persistent: bool = True) -> bool:
        if not persistent or keyring is None:
            self.session[config_name] = key
            return False
        try:
            keyring.set_password(SERVICE, config_name, key)
            return True
        except KeyringError:
            self.session[config_name] = key
            return False

    def get(self, config_name: str) -> str | None:
        if config_name in self.session:
            return self.session[config_name]
        if keyring is None:
            return None
        try:
            return keyring.get_password(SERVICE, config_name)
        except KeyringError:
            return None

    def delete(self, config_name: str) -> None:
        self.session.pop(config_name, None)
        with suppress(KeyringError):
            keyring.delete_password(SERVICE, config_name)

    def clear_session(self) -> None:
        self.session.clear()
