from httpx import AsyncClient


async def test_get_list_submenus(example_database, ac: AsyncClient):
    menu, submenu, _ = example_database
    response = await ac.get(f"/api/v1/menus/{menu.id}/submenus")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == [{"id": str(submenu.id),
                                "title": submenu.title,
                                "description": submenu.description,
                                "menu_id": str(menu.id)
                                }]


async def test_create_submenu(example_database, ac: AsyncClient):
    menu, submenu, _ = example_database
    response = await ac.post(f"/api/v1/menus/{menu.id}/submenus", json={
        "title": "My test submenu 1",
        "description": "My test submenu description 1",
        "menu_id": str(menu.id)
    })
    assert response.status_code == 201
    added_submenu_id = response.json()['id']

    added_submenu = await ac.get(f"/api/v1/menus/{menu.id}/submenus/{added_submenu_id}")
    assert added_submenu.json()['title'] == "My test submenu 1"
    assert added_submenu.json()['description'] == "My test submenu description 1"
    assert added_submenu.json()['menu_id'] == str(menu.id)


async def test_get_chosen_submenu(example_database, ac: AsyncClient):
    menu, submenu, _ = example_database
    response = await ac.get(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}")
    assert response.status_code == 200
    assert response.json()['title'] == submenu.title
    assert response.json()['description'] == submenu.description
    assert response.json()['menu_id'] == str(menu.id)


async def test_update_submenu(example_database, ac: AsyncClient):
    menu, submenu, _ = example_database
    response = await ac.patch(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}", json={
        "title": "My test updated submenu 1",
        "description": "My test updated submenu description 1"
    })
    assert response.status_code == 200

    updated_submenu = await ac.get(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}")
    assert updated_submenu.status_code == 200
    assert updated_submenu.json()['title'] == "My test updated submenu 1"
    assert updated_submenu.json()['description'] == "My test updated submenu description 1"


async def test_delete_submenu(example_database, ac: AsyncClient):
    menu, submenu, _ = example_database
    response = await ac.delete(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}")
    assert response.status_code == 200
    response = await ac.get(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}")
    assert response.status_code == 404
