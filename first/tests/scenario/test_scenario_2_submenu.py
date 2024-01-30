from httpx import AsyncClient


async def test_scenario_submenu(ac: AsyncClient):

    response_1 = await ac.post("/api/v1/menus", json={
        "title": "My menu 1",
        "description": "My menu description 1"
    })
    menu_id = response_1.json()['id']
    assert response_1.status_code == 201

    response_2 = await ac.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response_2.json() == []
    assert response_2.status_code == 200

    response_3 = await ac.post(f"/api/v1/menus/{menu_id}/submenus", json={
        "title": "My submenu 1",
        "description": "My submenu description 1"
    })
    submenu_id = response_3.json()['id']
    assert response_3.status_code == 201

    response_4 = await ac.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response_4.json() != []
    assert response_4.status_code == 200

    response_5 = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response_5.json()['id'] == submenu_id
    assert response_5.json()['title'] == 'My submenu 1'
    assert response_5.json()['description'] == 'My submenu description 1'
    assert response_5.status_code == 200

    response_6 = await ac.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', json={
            "title": "My updated submenu 1",
            "description": "My updated submenu description 1"
    })

    assert response_6.status_code == 200

    response_7 = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response_7.status_code == 200
    assert response_7.json() != []
    assert response_7.json()['title'] == 'My updated submenu 1'
    assert response_7.json()['description'] == 'My updated submenu description 1'

    response_8 = await ac.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response_8.status_code == 200

    response_9 = await ac.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response_9.status_code == 200
    assert response_9.json() == []

    response_10 = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response_10.status_code == 404
    assert response_10.json()['detail'] == 'submenu not found'

    response_11 = await ac.delete(f"/api/v1/menus/{menu_id}")
    assert response_11.status_code == 200

    response_12 = await ac.get("/api/v1/menus")
    assert response_12.status_code == 200
    assert response_12.json() == []
