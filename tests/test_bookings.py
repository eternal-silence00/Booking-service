async def _create_room_with_slot(async_client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    room = await async_client.post("/rooms", json={"name": "Room A", "capacity": 5}, headers=headers)
    room_id = room.json()["id"]
    slot = await async_client.post(f"/rooms/{room_id}/slots",
                                   json={"start_time": "09:00", "end_time": "11:00"}, headers=headers)
    return slot.json()["id"]    

async def test_create_booking(async_client, user_token, admin_token):
    slot_id = await _create_room_with_slot(async_client, admin_token)
    headers = {"Authorization": f"Bearer {user_token}"}
    resp = await async_client.post("/bookings",
                                   json={"slot_id": slot_id, "booking_date": "2026-07-01"}, headers=headers)
    assert resp.status_code == 201

async def test_booking_conflict(async_client, user_token, admin_token):
    slot_id = await _create_room_with_slot(async_client, admin_token)
    headers = {"Authorization": f"Bearer {user_token}"}
    body = {"slot_id": slot_id, "booking_date": "2026-07-01"}
    await async_client.post("/bookings", json=body, headers=headers)
    resp = await async_client.post("/bookings", json=body, headers=headers)
    assert resp.status_code == 409

async def test_booking_nonexistent_slot(async_client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    resp = await async_client.post("/bookings",
                                   json={"slot_id": 999, "booking_date": "2026-07-01"}, headers=headers)
    assert resp.status_code == 404

async def test_get_my_bookings(async_client, user_token, admin_token):
    slot_id = await _create_room_with_slot(async_client, admin_token)
    headers = {"Authorization": f"Bearer {user_token}"}
    await async_client.post("/bookings", json={"slot_id": slot_id, "booking_date": "2026-07-01"}, headers=headers)
    resp = await async_client.get("/bookings/me", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 1

async def test_cancel_own_booking(async_client, user_token, admin_token):
    slot_id = await _create_room_with_slot(async_client, admin_token)
    headers = {"Authorization": f"Bearer {user_token}"}
    booking = await async_client.post("/bookings", json={"slot_id": slot_id, "booking_date": "2026-07-01"}, headers=headers)
    booking_id = booking.json()["id"]
    resp = await async_client.delete(f"/bookings/{booking_id}", headers=headers)
    assert resp.status_code == 204
    
async def test_cancel_other_user_booking_forbidden(async_client, user_token, admin_token):
    slot_id = await _create_room_with_slot(async_client, admin_token)
    booking = await async_client.post("/bookings",
        json={"slot_id": slot_id, "booking_date": "2026-07-01"},
        headers={"Authorization": f"Bearer {user_token}"})
    booking_id = booking.json()["id"]
    await async_client.post("/auth/register", json={"email": "user2@test.com", "password": "test12345"})
    login = await async_client.post("/auth/login", json={"email": "user2@test.com", "password": "test12345"})
    user2_token = login.json()["access_token"]
    resp = await async_client.delete(f"/bookings/{booking_id}",
        headers={"Authorization": f"Bearer {user2_token}"})
    assert resp.status_code == 403

async def test_admin_can_cancel_any_booking(async_client, user_token, admin_token):
    slot_id = await _create_room_with_slot(async_client, admin_token)
    booking = await async_client.post("/bookings",
        json={"slot_id": slot_id, "booking_date": "2026-07-01"},
        headers={"Authorization": f"Bearer {user_token}"})
    booking_id = booking.json()["id"]
    resp = await async_client.delete(f"/bookings/{booking_id}",
        headers={"Authorization": f"Bearer {admin_token}"})
    assert resp.status_code == 204
    
async def test_availability(async_client, user_token, admin_token):
    slot_id = await _create_room_with_slot(async_client, admin_token)
    headers = {"Authorization": f"Bearer {user_token}"}
    resp = await async_client.get("/availability?date=2026-07-01", headers=headers)
    assert resp.status_code == 200
    assert resp.json()[0]["slots"][0]["is_available"] is True
    await async_client.post("/bookings", json={"slot_id": slot_id, "booking_date": "2026-07-01"}, headers=headers)
    resp = await async_client.get("/availability?date=2026-07-01", headers=headers)
    assert resp.json()[0]["slots"][0]["is_available"] is False