import uuid

from httpx import AsyncClient

menu_id: uuid
submenu_id: uuid


async def test_add_menu(ac: AsyncClient):
    global menu_id
    response = await ac.post("/api/v1/menus", json={
        "title": "My menu 1",
        "description": "My menu description 1"
    })
    menu_id = response.json()['id']
    assert response.status_code == 201


async def test_add_submenu(ac: AsyncClient):
    global submenu_id
    response = await ac.post(f"/api/v1/menus/{menu_id}/submenus", json={
        "title": "My submenu 1",
        "description": "My submenu description 1"
    })
    submenu_id = response.json()['id']
    assert response.status_code == 201


async def test_add_dish_1(ac: AsyncClient):
    response = await ac.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json={
        "title": "My dish 2",
        "description": "My dish description 2",
        "price": "13.50"
    })
    assert response.status_code == 201


async def test_add_dish_2(ac: AsyncClient):
    response = await ac.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json={
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    })
    assert response.status_code == 201


async def test_get_chosen_menu(ac: AsyncClient):
    global submenu_id
    response = await ac.get(f"/api/v1/menus/{menu_id}")
    assert response.json()['submenus_count'] == 1
    assert response.json()['dishes_count'] == 2
    assert response.status_code == 200


async def test_get_chosen_submenu(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.json()['dishes_count'] == 2
    assert response.status_code == 200


async def test_delete_chosen_submenu(ac: AsyncClient):
    response = await ac.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200


async def test_get_list_submenus(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.json() == []
    assert response.status_code == 200


async def test_get_list_dishes(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert response.json() == []
    assert response.status_code == 200


async def test_get_chosen_menu_2(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert response.json()['submenus_count'] == 0
    assert response.json()['dishes_count'] == 0


async def test_delete_chosen_menu(ac: AsyncClient):
    response = await ac.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200


async def test_get_list_menus(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus")
    assert response.json() == []
    assert response.status_code == 200
