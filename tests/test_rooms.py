async def test_create_room_as_admin(async_client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = await async_client.post("/rooms", json={"name": "Room A", "capacity": 5}, headers=headers)
    assert resp.status_code == 201
    assert resp.json()["name"] == "Room A"

async def test_create_room_as_user_forbidden(async_client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    resp = await async_client.post("/rooms", json={"name": "Room A", "capacity": 5}, headers=headers)
    assert resp.status_code == 403         

async def test_create_room_unauthorized(async_client):
    resp = await async_client.post("/rooms", json={"name": "Room A", "capacity": 5})
    assert resp.status_code in (401, 403)   

async def test_get_rooms(async_client, admin_token, user_token):
    headers_admin = {"Authorization": f"Bearer {admin_token}"}
    await async_client.post("/rooms", json={"name": "Room A", "capacity": 5}, headers=headers_admin)
    resp = await async_client.get("/rooms", headers={"Authorization": f"Bearer {user_token}"})
    assert resp.status_code == 200
    assert len(resp.json()) == 1

async def test_create_slot_as_admin(async_client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    room = await async_client.post("/rooms", json={"name": "Room A", "capacity": 5}, headers=headers)
    room_id = room.json()["id"]
    resp = await async_client.post(f"/rooms/{room_id}/slots",
                                   json={"start_time": "09:00", "end_time": "11:00"}, headers=headers)
    assert resp.status_code == 201

async def test_create_slot_invalid_time(async_client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    room = await async_client.post("/rooms", json={"name": "Room A", "capacity": 5}, headers=headers)
    room_id = room.json()["id"]
    resp = await async_client.post(f"/rooms/{room_id}/slots",
                                   json={"start_time": "11:00", "end_time": "09:00"}, headers=headers)
    assert resp.status_code == 422