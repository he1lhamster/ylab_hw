import uuid

from httpx import AsyncClient


menu_id: uuid


async def test_get_menus_0(ac: AsyncClient):
    response = await ac.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() == []


async def test_add_menu(ac: AsyncClient):
    global menu_id
    response = await ac.post("/api/v1/menus", json={
        "title": "My menu 1",
        "description": "My menu description 1"
    }
                             )
    menu_id = response.json()['id']
    assert response.status_code == 201


async def test_get_menus_1(ac: AsyncClient):
    response = await ac.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() != []
    assert response.json()[0]['title'] == 'My menu 1'
    assert response.json()[0]['description'] == 'My menu description 1'



async def test_patch_menu(ac: AsyncClient):
    response = await ac.patch(f'/api/v1/menus/{menu_id}', json={
            "title": "My updated menu 1",
            "description": "My updated menu description 1"
    })

    assert response.status_code == 200


async def test_patched_menu(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert response.json() != []
    assert response.json()['title'] == 'My updated menu 1'
    assert response.json()['description'] == 'My updated menu description 1'


async def test_delete_menu(ac: AsyncClient):
    response = await ac.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200


async def test_get_menus_2(ac: AsyncClient):
    response = await ac.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() == []


async def test_deleted_menu(ac: AsyncClient):
    response = await ac.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 404
    assert response.json()['detail'] == 'menu not found'
