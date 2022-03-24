def test_basic_call(client):
    response = client.get('/hello')
    assert b'Welcome to Tour de Flask!' in response.data
