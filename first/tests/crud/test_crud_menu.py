import uuid

from httpx import AsyncClient


menu_id: uuid


async def test_get_list_menus(ac: AsyncClient):
    response = await ac.get("/api/v1/menus")
    assert isinstance(response.json(), list)
    assert response.status_code == 200


async def test_create_menu(ac: AsyncClient):
    global menu_id
    response = await ac.post("/api/v1/menus", json={
        "title": "My menu 1",
        "description": "My menu description 1"
    })
    menu_id = response.json()['id']
    assert response.status_code == 201


async def test_get_chosen_menu(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200


async def test_update_menu(ac: AsyncClient):
    response = await ac.patch(f"/api/v1/menus/{menu_id}", json={
        "title": "My updated menu 1",
        "description": "My updated menu description 1"
    })
    assert response.status_code == 200


async def test_delete_menu(ac: AsyncClient):
    response = await ac.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200


async def test_get_chosen_menu_2(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 404


async def test_update_menu_2(ac: AsyncClient):
    response = await ac.patch(f"/api/v1/menus/{menu_id}", json={
        "title": "My updated menu 1-1",
        "description": "My updated menu description 1-1"
    })
    assert response.status_code == 404

