import urllib.request as req
from datetime import datetime, timezone
from random import randint

import pytest
from discord_webhook import DiscordWebhook
from pytest import MonkeyPatch

from ipget.alchemy import SQLite


class FakeResponse:
    def __init__(self, status_code: int) -> None:
        self.status_code: int = status_code

    def getcode(self):
        return self.status_code


@pytest.fixture
def mock_discord_response(monkeypatch: MonkeyPatch):
    def response_200(*args, **kwargs):
        return FakeResponse(200)

    monkeypatch.setenv("IPGET_DISCORD_WEBHOOK", "https://test.example.com")
    monkeypatch.setattr(DiscordWebhook, "execute", response_200)


@pytest.fixture
def mock_healthcheck_response(monkeypatch: MonkeyPatch):
    def response_200(*args, **kwargs):
        return FakeResponse(200)

    monkeypatch.setenv("IPGET_HEALTHCHECK_SERVER", "https://hc.example.com")
    monkeypatch.setenv("IPGET_HEALTHCHECK_UUID", "test-uuid")
    monkeypatch.setattr(req, "urlopen", response_200)


@pytest.fixture
def sqlite_in_memory(monkeypatch: MonkeyPatch):
    monkeypatch.setenv("IPGET_SQLITE_DATABASE", ":memory:")
    return SQLite()


@pytest.fixture
def ip_data_static() -> tuple[datetime, str]:
    return (datetime(1963, 11, 23, 17, 16), "10.10.10.0")


@pytest.fixture
def ip_data_random() -> tuple[datetime, str]:
    dt = datetime.now(timezone.utc).replace(microsecond=0)
    ip = ".".join(str(randint(0, 255)) for _ in range(4))
    return dt, ip
