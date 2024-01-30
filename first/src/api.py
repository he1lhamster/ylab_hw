from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from schemas import *
from orm import AsyncORM

router = APIRouter(prefix='/api/v1')


# MENU
@router.get(
    "/menus",
    responses={
        200: {"description": "Successful response."},
    },
)
async def get_menus(a_orm: AsyncORM = Depends()):
    result = await a_orm.get_menus()
    result = jsonable_encoder(result) if result else []
    return JSONResponse(content=result, status_code=200)


@router.get(
    "/menus/{api_test_menu_id}",
    responses={
        200: {"description": "Successful response."},
        404: {"description": "Menu not found"},
    },
)
async def get_menu(
        api_test_menu_id: str,
        a_orm: AsyncORM = Depends()
):
    result = await a_orm.get_menu(api_test_menu_id)
    if not result:
        raise HTTPException(status_code=404, detail='menu not found')

    content = jsonable_encoder(result)
    content['submenus_count'], content['dishes_count'] = await a_orm.menu_count_submenus_and_dishes(api_test_menu_id)
    # content['submenus_count'] = await a_orm.menu_count_submenus(api_test_menu_id)
    # content['dishes_count'] = await a_orm.menu_count_dishes(api_test_menu_id)
    return JSONResponse(content=content, status_code=200)


@router.post(
    "/menus",
    responses={
        201: {"description": "Successful response."},
    },
)
async def create_menu(
        menu: MenuSchema,
        a_orm: AsyncORM = Depends()
):
    created_menu = await a_orm.create_menu(menu)
    content_response = jsonable_encoder(created_menu)
    return JSONResponse(content=content_response, status_code=201)


@router.patch(
    "/menus/{api_test_menu_id}",
    responses={
        200: {"description": "Successful response."},
        404: {"description": "Menu not found"},
    },
)
async def update_menu(
        api_test_menu_id: str,
        menu: MenuSchema,
        a_orm: AsyncORM = Depends()
):
    result = await a_orm.update_menu(api_test_menu_id, menu)
    result = jsonable_encoder(result)
    if not result:
        raise HTTPException(status_code=404, detail='menu not found')
    return JSONResponse(content=result, status_code=200)


@router.delete(
    "/menus/{api_test_menu_id}",
    responses={
        200: {"description": "Successful response."},
    },
)
async def delete_menu(
        api_test_menu_id: str,
        a_orm: AsyncORM = Depends()
):
    await a_orm.delete_menu(api_test_menu_id)
    return JSONResponse(status_code=200, content={"message": "The menu has been deleted",
                                                  "status": True})


# SUBMENU -------------------

@router.get(
    "/menus/{api_test_menu_id}/submenus",
    responses={
        200: {"description": "Successful response ."},
    },
)
async def get_submenus(
        api_test_menu_id: str,
        a_orm: AsyncORM = Depends(),
):
    result = await a_orm.get_submenus(api_test_menu_id)
    result = jsonable_encoder(result) if result else []
    return JSONResponse(content=result, status_code=200)


@router.get(
    "/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}",
    responses={
        200: {"description": "Successful response"},
        404: {"description": "Submenu not found"},
    },
)
async def get_submenu(
        api_test_menu_id: str,
        api_test_submenu_id: str,
        a_orm: AsyncORM = Depends()
):

    result = await a_orm.get_submenu(api_test_submenu_id)
    if not result:
        raise HTTPException(status_code=404, detail='submenu not found')
    content = jsonable_encoder(result)
    content['dishes_count'] = await a_orm.count_dishes(api_test_submenu_id)
    return JSONResponse(content=content, status_code=200)


@router.post(
    "/menus/{api_test_menu_id}/submenus",
    responses={
        200: {"description": "Successful response."},
    },
)
async def create_submenu(api_test_menu_id: str, submenu: SubmenuSchema, a_orm: AsyncORM = Depends()):
    created_submenu = await a_orm.create_submenu(submenu, api_test_menu_id)
    content_response = jsonable_encoder(created_submenu)
    return JSONResponse(content=content_response, status_code=201)


@router.patch(
    "/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}",
    responses={
        200: {"description": "Successful response."},
        404: {"description": "Submenu not found"},
    },
)
async def update_submenu(
        api_test_menu_id: str,
        api_test_submenu_id: str,
        submenu: SubmenuSchema,
        a_orm: AsyncORM = Depends()
):
    result = await a_orm.update_submenu(submenu, api_test_submenu_id)
    result = jsonable_encoder(result)
    if not result:
        raise HTTPException(status_code=404, detail='submenu not found')
    return JSONResponse(content=result, status_code=200)


@router.delete(
    "/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}",
    responses={
        204: {"description": "Successful response."},
    },
)
async def delete_submenu(
        api_test_menu_id: str,
        api_test_submenu_id: str,
        a_orm: AsyncORM = Depends()
):
    await a_orm.delete_submenu(api_test_submenu_id)
    return JSONResponse(status_code=200, content={"message": "The submenu has been deleted",
                                                  "status": True})


# DISH -------------------
@router.get(
    "/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes",
    responses={
        200: {"description": "Successful response ."},
    },
)
async def get_dishes(
        api_test_menu_id: str,
        api_test_submenu_id: str,
        a_orm: AsyncORM = Depends()
):
    result = await a_orm.get_dishes(api_test_submenu_id)
    result = jsonable_encoder(result)
    return JSONResponse(content=result, status_code=200)


@router.get(
    "/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}",
    responses={
        200: {"description": "Successful response"},
        404: {"description": "Dish not found"},
    },
)
async def get_dish(
        api_test_menu_id: str,
        api_test_submenu_id: str,
        api_test_dish_id: str,
        a_orm: AsyncORM = Depends()
):
    result = await a_orm.get_dish(api_test_dish_id)
    res = jsonable_encoder(result)
    if not res:
        raise HTTPException(status_code=404, detail='dish not found')
    res['price'] = str("{:.2f}".format(res['price']))
    return JSONResponse(content=res, status_code=200)


@router.post(
    "/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes",
    responses={
        201: {"description": "Successful response."},
    },
)
async def create_dish(
        api_test_menu_id: str,
        api_test_submenu_id: str,
        dish: DishSchema,
        a_orm: AsyncORM = Depends()
):
    created_dish = await a_orm.create_dish(dish, api_test_submenu_id)
    content_response = jsonable_encoder(created_dish)
    return JSONResponse(content=content_response, status_code=201)


@router.patch(
    "/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}",
    responses={
        200: {"description": "Successful response."},
        404: {"description": "Dish not found"},
    },
)
async def update_dish(
        api_test_menu_id: str,
        api_test_submenu_id: str,
        api_test_dish_id: str,
        dish: DishSchema,
        a_orm: AsyncORM = Depends()
):
    result = await a_orm.update_dish(dish, api_test_dish_id)
    res = jsonable_encoder(result)
    if not res:
        raise HTTPException(status_code=404, detail='dish not found')
    res['price'] = str("{:.2f}".format(res['price']))
    return JSONResponse(content=res, status_code=200)


@router.delete(
    "/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}",
    responses={
        204: {"description": "Successful response."},
    },
)
async def delete_dish(
        api_test_menu_id: str,
        api_test_submenu_id: str,
        api_test_dish_id: str,
        a_orm: AsyncORM = Depends()
):
    await a_orm.delete_dish(api_test_dish_id)
    return JSONResponse(status_code=200, content={"message": "The dish has been deleted",
                                                  "status": True})
