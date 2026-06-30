async def test_register(async_client):
    resp = await async_client.post("/auth/register", json={"email": "a@test.com", "password": "test12345"})
    assert resp.status_code == 201
    assert resp.json()["email"] == "a@test.com"
    assert resp.json()["role"] == "employee"     

async def test_register_duplicate(async_client):
    await async_client.post("/auth/register", json={"email": "a@test.com", "password": "test12345"})
    resp = await async_client.post("/auth/register", json={"email": "a@test.com", "password": "test12345"})
    assert resp.status_code == 400

async def test_login(async_client):
    await async_client.post("/auth/register", json={"email": "a@test.com", "password": "test12345"})
    resp = await async_client.post("/auth/login", json={"email": "a@test.com", "password": "test12345"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()

async def test_login_wrong_password(async_client):
    await async_client.post("/auth/register", json={"email": "a@test.com", "password": "test12345"})
    resp = await async_client.post("/auth/login", json={"email": "a@test.com", "password": "wrongpass1"})
    assert resp.status_code == 401

async def test_register_short_password(async_client):
    resp = await async_client.post("/auth/register", json={"email": "a@test.com", "password": "short"})
    assert resp.status_code == 422       