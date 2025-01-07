import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("room_id, date_from, date_to, booked_rooms, status_code", [
    (1, "2030-01-01", "2030-01-09", 3, 200),
    (1, "2030-01-01", "2030-01-09", 4, 200),
    (1, "2030-01-01", "2030-01-09", 5, 200),
    (1, "2030-01-01", "2030-01-09", 6, 200),
    (1, "2030-01-01", "2030-01-09", 7, 409),
    (1, "2030-01-01", "2030-01-09", 7, 409)
])
async def test_add_and_get_booking(authenticated_ac: AsyncClient, room_id, date_from, date_to, status_code, booked_rooms):
    response = await authenticated_ac.post("/booking", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })

    assert response.status_code == status_code

    response = await authenticated_ac.get("/booking")

    assert len(response.json()) == booked_rooms