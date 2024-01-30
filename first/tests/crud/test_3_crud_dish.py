from httpx import AsyncClient


async def test_get_list_dishes(example_database, ac: AsyncClient):
    menu, submenu, dish = example_database
    response = await ac.get(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == [{"id": str(dish.id),
                                "title": dish.title,
                                "description": dish.description,
                                "price": dish.price,
                                "submenu_id": str(submenu.id)
                                }]


async def test_create_dish(example_database, ac: AsyncClient):
    menu, submenu, dish = example_database
    response = await ac.post(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes", json={
        "title": "My test dish 1",
        "description": "My test dish description 1",
        "price": "6.95",
        "submenu_id": str(submenu.id)
    })
    assert response.status_code == 201
    added_dish_id = response.json()['id']

    added_dish = await ac.get(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{added_dish_id}")
    assert added_dish.json()['title'] == "My test dish 1"
    assert added_dish.json()['description'] == "My test dish description 1"
    assert added_dish.json()['price'] == str("{:.2f}".format(6.95))
    assert added_dish.json()['submenu_id'] == str(submenu.id)


async def test_get_chosen_dish(example_database, ac: AsyncClient):
    menu, submenu, dish = example_database
    response = await ac.get(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}")
    assert response.status_code == 200
    assert response.json()['title'] == dish.title
    assert response.json()['description'] == dish.description
    assert response.json()['price'] == str("{:.2f}".format(dish.price))
    assert response.json()['submenu_id'] == str(submenu.id)


async def test_update_dish(example_database, ac: AsyncClient):
    menu, submenu, dish = example_database
    response = await ac.patch(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}", json={
        "title": "My test updated dish 1",
        "description": "My test updated dish description 1",
        "price": "99.12"
    })
    assert response.status_code == 200

    updated_dish = await ac.get(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}")
    assert updated_dish.status_code == 200
    assert updated_dish.json()['title'] == "My test updated dish 1"
    assert updated_dish.json()['description'] == "My test updated dish description 1"
    assert updated_dish.json()['price'] == "99.12"

async def test_delete_dish(example_database, ac: AsyncClient):
    menu, submenu, dish = example_database
    response = await ac.delete(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}")
    assert response.status_code == 200
    response = await ac.get(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}")
    assert response.status_code == 404
