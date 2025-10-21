
import pytest
from fastapi.testclient import TestClient

from app.db import Base, engine
from app.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Recreate tables fresh for each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_and_get_string():
    r = client.post("/strings", json={"value": "racecar"})
    assert r.status_code == 201
    assert r.json()["properties"]["is_palindrome"] is True

    r2 = client.get("/strings/racecar")
    assert r2.status_code == 200

def test_conflict():
    client.post("/strings", json={"value": "hello"})
    r = client.post("/strings", json={"value": "hello"})
    assert r.status_code == 409

def test_filter():
    client.post("/strings", json={"value": "level"})
    r = client.get("/strings?is_palindrome=true&word_count=1")
    assert r.status_code == 200

def test_nl_filter():
    client.post("/strings", json={"value": "madam"})
    r = client.get("/strings/filter-by-natural-language", params={"query": "all single word palindromic strings"})
    assert r.status_code == 200

def test_delete():
    client.post("/strings", json={"value": "temp"})
    r = client.delete("/strings/temp")
    assert r.status_code == 204
