import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Health check should always return ok"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_mirror_endpoint():
    """Mirror endpoint should transform the word correctly"""
    response = client.get("/api/mirror?word=fOoBar25")
    assert response.status_code == 200
    assert response.json() == {"transformed": "52RAbOoF"}

def test_mirror_with_simple_word():
    """Test with a simple word"""
    response = client.get("/api/mirror?word=test")
    assert response.status_code == 200
    assert response.json() == {"transformed": "TSET"}

def test_mirror_missing_parameter():
    """Should return 422 if word parameter is missing"""
    response = client.get("/api/mirror")
    assert response.status_code == 422
