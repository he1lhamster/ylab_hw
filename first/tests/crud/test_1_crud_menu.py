from httpx import AsyncClient


async def test_get_list_menus(example_database, ac: AsyncClient):
    menu, _, _ = example_database
    response = await ac.get("/api/v1/menus")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == [{"id": str(menu.id),
                                "title": menu.title,
                                "description": menu.description
                                }]


async def test_create_menu(ac: AsyncClient):
    response = await ac.post("/api/v1/menus", json={
        "title": "My menu 1",
        "description": "My menu description 1"
    })
    added_menu_id = response.json()['id']
    assert response.status_code == 201

    added_menu = await ac.get(f"/api/v1/menus/{added_menu_id}")
    assert added_menu.json()['title'] == 'My menu 1'
    assert added_menu.json()['description'] == 'My menu description 1'


async def test_get_chosen_menu(example_database, ac: AsyncClient):
    menu, _, _ = example_database
    response = await ac.get(f"/api/v1/menus/{menu.id}")
    assert response.status_code == 200
    assert response.json()['title'] == menu.title
    assert response.json()['description'] == menu.description


async def test_update_menu(example_database, ac: AsyncClient):
    menu, _, _ = example_database
    response = await ac.patch(f"/api/v1/menus/{menu.id}", json={
        "title": "My test updated menu 1",
        "description": "My test updated menu description 1"
    })
    assert response.status_code == 200

    updated_menu = await ac.get(f"/api/v1/menus/{menu.id}")
    assert updated_menu.status_code == 200
    assert updated_menu.json()['title'] == "My test updated menu 1"
    assert updated_menu.json()['description'] == "My test updated menu description 1"


async def test_delete_menu(example_database, ac: AsyncClient):
    menu, _, _ = example_database
    response = await ac.delete(f"/api/v1/menus/{menu.id}")
    assert response.status_code == 200
    response = await ac.get(f"/api/v1/menus/{menu.id}")
    assert response.status_code == 404

