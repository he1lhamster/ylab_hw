import uuid

from httpx import AsyncClient

menu_id: uuid
submenu_id: uuid
dish_id: uuid


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


async def test_get_list_dishes_1(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert response.json() == []
    assert response.status_code == 200


async def test_add_dish(ac: AsyncClient):
    global dish_id
    response = await ac.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json={
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    })
    dish_id = response.json()['id']
    assert response.status_code == 201


async def test_get_list_dishes_2(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert response.json() != []
    assert response.status_code == 200


async def test_get_chosen_dish_1(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.json() != []
    assert response.json()['id'] == dish_id
    assert response.json()['price'] == "12.50"
    assert response.json()['title'] == "My dish 1"
    assert response.json()['description'] == 'My dish description 1'
    assert response.status_code == 200


async def test_update_dish(ac: AsyncClient):
    response = await ac.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", json={
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": "14.50"
    })
    assert response.status_code == 200


async def test_get_chosen_dish_2(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200
    assert response.json() != []
    assert response.json()['id'] == dish_id
    assert response.json()['price'] == "14.50"
    assert response.json()['title'] == "My updated dish 1"
    assert response.json()['description'] == 'My updated dish description 1'
    assert response.status_code == 200



async def test_delete_dish(ac: AsyncClient):
    response = await ac.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200


async def test_get_list_dishes_3(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert response.json() == []
    assert response.status_code == 200


async def test_get_deleted_dish(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 404
    assert response.json()['detail'] == 'dish not found'


async def test_delete_submenu(ac: AsyncClient):
    response = await ac.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200


async def test_deleted_submenu(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 404
    assert response.json()['detail'] == 'submenu not found'


async def test_delete_menu(ac: AsyncClient):
    response = await ac.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200


async def test_get_list_menus(ac: AsyncClient):
    response = await ac.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() == []
