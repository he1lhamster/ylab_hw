from httpx import AsyncClient


async def test_scenario_menu(ac: AsyncClient):
    response_1 = await ac.get("/api/v1/menus")
    assert response_1.status_code == 200
    assert response_1.json() == []

    response_2 = await ac.post("/api/v1/menus", json={
        "title": "My menu 1",
        "description": "My menu description 1"
    }
                             )
    menu_id = response_2.json()['id']
    assert response_2.status_code == 201

    response_3 = await ac.get("/api/v1/menus")
    assert response_3.status_code == 200
    assert response_3.json() != []
    assert response_3.json()[0]['title'] == 'My menu 1'
    assert response_3.json()[0]['description'] == 'My menu description 1'

    response_4 = await ac.patch(f'/api/v1/menus/{menu_id}', json={
            "title": "My updated menu 1",
            "description": "My updated menu description 1"
    })

    assert response_4.status_code == 200

    response_5 = await ac.get(f"/api/v1/menus/{menu_id}")
    assert response_5.status_code == 200
    assert response_5.json() != []
    assert response_5.json()['title'] == 'My updated menu 1'
    assert response_5.json()['description'] == 'My updated menu description 1'

    response_6 = await ac.delete(f"/api/v1/menus/{menu_id}")
    assert response_6.status_code == 200

    response_7 = await ac.get("/api/v1/menus")
    assert response_7.status_code == 200
    assert response_7.json() == []

    response_8 = await ac.get(f"/api/v1/menus/{menu_id}")
    assert response_8.status_code == 404
    assert response_8.json()['detail'] == 'menu not found'
