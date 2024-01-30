from httpx import AsyncClient


async def test_scenario_dish(ac: AsyncClient):
    response_1 = await ac.post("/api/v1/menus", json={
        "title": "My menu 1",
        "description": "My menu description 1"
    })
    menu_id = response_1.json()['id']
    assert response_1.status_code == 201

    response_2 = await ac.post(f"/api/v1/menus/{menu_id}/submenus", json={
        "title": "My submenu 1",
        "description": "My submenu description 1"
    })
    submenu_id = response_2.json()['id']
    assert response_2.status_code == 201

    response_3 = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert response_3.json() == []
    assert response_3.status_code == 200

    response_4 = await ac.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json={
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    })
    dish_id = response_4.json()['id']
    assert response_4.status_code == 201

    response_5 = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert response_5.json() != []
    assert response_5.status_code == 200

    response_6 = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response_6.json() != []
    assert response_6.json()['id'] == dish_id
    assert response_6.json()['price'] == "12.50"
    assert response_6.json()['title'] == "My dish 1"
    assert response_6.json()['description'] == 'My dish description 1'
    assert response_6.status_code == 200

    response_7 = await ac.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", json={
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": "14.50"
    })
    assert response_7.status_code == 200

    response_8 = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response_8.status_code == 200
    assert response_8.json() != []
    assert response_8.json()['id'] == dish_id
    assert response_8.json()['price'] == "14.50"
    assert response_8.json()['title'] == "My updated dish 1"
    assert response_8.json()['description'] == 'My updated dish description 1'
    assert response_8.status_code == 200

    response_9 = await ac.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response_9.status_code == 200

    response_10 = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert response_10.json() == []
    assert response_10.status_code == 200

    response_11 = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response_11.status_code == 404
    assert response_11.json()['detail'] == 'dish not found'

    response_12 = await ac.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response_12.status_code == 200

    response_13 = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response_13.status_code == 404
    assert response_13.json()['detail'] == 'submenu not found'

    response_14 = await ac.delete(f"/api/v1/menus/{menu_id}")
    assert response_14.status_code == 200

    response_15 = await ac.get("/api/v1/menus")
    assert response_15.status_code == 200
    assert response_15.json() == []
