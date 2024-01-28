import uuid

from httpx import AsyncClient


menu_id: uuid
submenu_id: uuid


async def test_add_submenu(ac: AsyncClient):
    global menu_id
    global submenu_id

    _response = await ac.post("/api/v1/menus", json={
        "title": "My menu 1",
        "description": "My menu description 1"
    })
    menu_id = _response.json()['id']
    response = await ac.post(f"/api/v1/menus/{menu_id}/submenus", json={
        "title": "My submenu 1",
        "description": "My submenu description 1"
    })
    submenu_id = response.json()['id']
    assert response.status_code == 201


async def test_get_list_submenus(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus")
    assert isinstance(response.json(), list)
    assert response.status_code == 200


async def test_get_chosen_submenu(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200


async def test_update_submenu(ac: AsyncClient):
    response = await ac.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', json={
            "title": "My updated submenu 1",
            "description": "My updated submenu description 1"
    })

    assert response.status_code == 200


async def test_delete_submenu(ac: AsyncClient):
    response = await ac.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200


async def test_chosen_submenu_2(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 404


async def test_update_submenu_2(ac: AsyncClient):
    response = await ac.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', json={
            "title": "My updated submenu 1-1",
            "description": "My updated submenu description 1-1"
    })

    assert response.status_code == 404


async def test_delete_menu(ac: AsyncClient):
    response = await ac.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
