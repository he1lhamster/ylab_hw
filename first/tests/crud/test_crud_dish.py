import uuid

from httpx import AsyncClient


menu_id: uuid
submenu_id: uuid
dish_id: uuid


async def test_add_dish(ac: AsyncClient):
    global menu_id
    global submenu_id
    global dish_id

    response_1 = await ac.post("/api/v1/menus", json={
        "title": "My menu 1",
        "description": "My menu description 1"
    })
    menu_id = response_1.json()['id']

    response_2 = await ac.post(f"/api/v1/menus/{menu_id}/submenus", json={
        "title": "My submenu 1",
        "description": "My submenu description 1"
    })
    submenu_id = response_2.json()['id']

    response_3 = await ac.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json={
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    })
    dish_id = response_3.json()['id']
    assert response_3.status_code == 201


async def test_get_list_dishes(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert isinstance(response.json(), list)
    assert response.status_code == 200


async def test_get_chosen_dish(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200


async def test_update_dish(ac: AsyncClient):
    response = await ac.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", json={
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": "14.50"
    })
    assert response.status_code == 200


async def test_delete_dish(ac: AsyncClient):
    response = await ac.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200


async def test_get_chosen_dish_2(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 404


async def test_update_dish_2(ac: AsyncClient):
    response = await ac.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
                              json={
                                  "title": "My updated dish 1-1",
                                  "description": "My updated dish description 1-1",
                                  "price": "15.50"
                              })
    assert response.status_code == 404


async def test_delete_menu(ac: AsyncClient):
    response = await ac.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200

