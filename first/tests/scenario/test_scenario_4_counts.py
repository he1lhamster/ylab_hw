from httpx import AsyncClient


async def test_scenario_counts(ac: AsyncClient):
    response_1 = await ac.post("/api/v1/menus", json={
        "title": "My menu 1",
        "description": "My menu description 1"
    })
    assert response_1.status_code == 201
    menu_id = response_1.json()['id']

    response_2 = await ac.post(f"/api/v1/menus/{menu_id}/submenus", json={
        "title": "My submenu 1",
        "description": "My submenu description 1"
    })
    assert response_2.status_code == 201
    submenu_id = response_2.json()['id']

    response_3 = await ac.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json={
        "title": "My dish 2",
        "description": "My dish description 2",
        "price": "13.50"
    })
    assert response_3.status_code == 201

    response_4 = await ac.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json={
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    })
    assert response_4.status_code == 201

    response_5 = await ac.get(f"/api/v1/menus/{menu_id}")
    assert response_5.json()['submenus_count'] == 1
    assert response_5.json()['dishes_count'] == 2
    assert response_5.status_code == 200

    response_6 = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response_6.json()['dishes_count'] == 2
    assert response_6.status_code == 200

    response_7 = await ac.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response_7.status_code == 200

    response_8 = await ac.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response_8.json() == []
    assert response_8.status_code == 200

    response_9 = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert response_9.json() == []
    assert response_9.status_code == 200

    response_10 = await ac.get(f"/api/v1/menus/{menu_id}")
    assert response_10.status_code == 200
    assert response_10.json()['submenus_count'] == 0
    assert response_10.json()['dishes_count'] == 0

    response_11 = await ac.delete(f"/api/v1/menus/{menu_id}")
    assert response_11.status_code == 200

    response_12 = await ac.get(f"/api/v1/menus")
    assert response_12.json() == []
    assert response_12.status_code == 200
