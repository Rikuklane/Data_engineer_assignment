

def test_greeting(client):
    response = client.get("/")
    assert "Hello, STACC!" in response.text


def test_info_all(client):
    response = client.get("/info")
    assert response.status_code == 200


def test_info_msft(client):
    response = client.get("/info/msft")
    assert response.status_code == 200


def test_historical_msft(client):
    response = client.get("/historical/msft")
    assert response.status_code == 200


def test_random(client):
    response = client.get("/random")
    assert response.status_code == 404
