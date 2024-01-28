import uuid

from httpx import AsyncClient


menu_id: uuid
submenu_id: uuid


async def test_scenario_add_menu(ac: AsyncClient):
    global menu_id
    response = await ac.post("/api/v1/menus", json={
        "title": "My menu 1",
        "description": "My menu description 1"
    })
    menu_id = response.json()['id']
    assert response.status_code == 201


async def test_scenario_get_list_submenus_1(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.json() == []
    assert response.status_code == 200


async def test_scenario_add_submenu(ac: AsyncClient):
    global submenu_id
    response = await ac.post(f"/api/v1/menus/{menu_id}/submenus", json={
        "title": "My submenu 1",
        "description": "My submenu description 1"
    })
    submenu_id = response.json()['id']
    assert response.status_code == 201


async def test_scenario_get_list_submenus_2(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.json() != []
    assert response.status_code == 200


async def test_scenario_get_chosen_submenu(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.json()['id'] == submenu_id
    assert response.json()['title'] == 'My submenu 1'
    assert response.json()['description'] == 'My submenu description 1'
    assert response.status_code == 200


async def test_scenario_patch_submenu(ac: AsyncClient):
    response = await ac.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', json={
            "title": "My updated submenu 1",
            "description": "My updated submenu description 1"
    })

    assert response.status_code == 200


async def test_scenario_get_patched_submenu(ac: AsyncClient):
    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200
    assert response.json() != []
    assert response.json()['title'] == 'My updated submenu 1'
    assert response.json()['description'] == 'My updated submenu description 1'


async def test_scenario_delete_submenu(ac: AsyncClient):
    response = await ac.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200


async def test_scenario_get_list_submenus_3(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200
    assert response.json() == []


async def test_scenario_deleted_submenu(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 404
    assert response.json()['detail'] == 'submenu not found'


async def test_scenario_delete_menu(ac: AsyncClient):
    response = await ac.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200


async def test_scenario_get_list_menus(ac: AsyncClient):
    response = await ac.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() == []
