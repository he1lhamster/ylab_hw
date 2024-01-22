from typing import List, Any

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import async_engine, get_async_session
from models import *
from models import Menu
from schemas import *


class AsyncORM:
    def __init__(self, session: Session = Depends(get_async_session)):
        self.session = session

    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    # MENU ---------------
    async def get_menu(self, menu_id: uuid) -> Menu | None:
        query = select(Menu).filter(Menu.id == menu_id)
        res = await self.session.scalar(query)
        return res

    async def get_menus(self, ) -> List[Menu]:
        query = select(Menu)
        result = await self.session.execute(query)
        menus = result.scalars().all()
        return menus

    async def insert_menu(self, menu: MenuSchema) -> Menu:
        new_menu = Menu(title=menu.title, description=menu.description)
        self.session.add(new_menu)
        await self.session.flush()
        await self.session.commit()
        return new_menu

    async def delete_menu(self, menu_id: uuid):
        menu_item = await self.session.get(Menu, menu_id)
        await self.session.delete(menu_item)
        await self.session.commit()

    async def update_menu(self, menu_id: uuid, menu: MenuSchema) -> Menu | None:
        menu_item = await self.session.get(Menu, menu_id)
        if not menu_item:
            return None
        menu_item.title = menu.title
        menu_item.description = menu.description
        await self.session.commit()
        await self.session.refresh(menu_item)
        return menu_item

    async def menu_count_submenus(self, menu_id: uuid) -> int:
        query = select(Submenu).filter(Submenu.menu_id == menu_id)
        result = await self.session.scalars(query)
        return len(list(result))

    async def menu_count_dishes(self, menu_id: uuid) -> int:
        query = select(Submenu).filter(Submenu.menu_id == menu_id)
        result = await self.session.scalars(query)
        count = 0
        for submenu in result:
            count += await self.count_dishes(submenu.id)
        return count

    # SUBMENU -------------
    async def get_submenus(self, menu_id: uuid) -> List[Submenu]:
        query = select(Submenu).filter(Submenu.menu_id == menu_id)
        result = await self.session.execute(query)
        submenus = result.scalars().all()
        return submenus

    async def get_submenu(self, submenu_id: uuid) -> Submenu:
        query = select(Submenu).filter(Submenu.id == submenu_id)
        res = await self.session.scalar(query)
        return res

    async def create_submenu(self, submenu: SubmenuSchema, menu_id: uuid) -> Submenu:
        new_submenu = Submenu(title=submenu.title, description=submenu.description, menu_id=menu_id)
        self.session.add(new_submenu)
        await self.session.flush()
        await self.session.commit()
        return new_submenu

    async def update_submenu(self, submenu: SubmenuSchema, submenu_id: uuid) -> Submenu | None:
        submenu_item = await self.session.get(Submenu, submenu_id)
        if not submenu_item:
            return None
        submenu_item.title = submenu.title
        submenu_item.description = submenu.description
        await self.session.commit()
        await self.session.refresh(submenu_item)
        return submenu_item

    async def delete_submenu(self, submenu_id: uuid):
        submenu_item = await self.session.get(Submenu, submenu_id)
        await self.session.delete(submenu_item)
        await self.session.commit()

    async def count_dishes(self, submenu_id: uuid) -> int:
        query = select(Dish).filter(Dish.submenu_id == submenu_id)
        result = await self.session.scalars(query)
        return len(list(result))

    # DISH-------------
    async def get_dishes(self, submenu_id: uuid) -> List[Dish] | None:
        query = select(Dish).filter(Dish.submenu_id == submenu_id)
        result = await self.session.execute(query)
        dishes = result.scalars().all()
        return dishes

    async def get_dish(self, dish_id: uuid) -> Dish:
        query = select(Dish).filter(Dish.id == dish_id)
        res = await self.session.scalar(query)
        return res

    async def create_dish(self, dish: DishSchema, submenu_id: uuid) -> Dish:
        new_dish = Dish(
            title=dish.title,
            description=dish.description,
            price=str(dish.price),
            submenu_id=submenu_id,
        )
        self.session.add(new_dish)
        await self.session.flush()
        await self.session.commit()
        return new_dish

    async def update_dish(self, dish: DishSchema, dish_id: uuid) -> Dish:
        dish_item = await self.session.get(Dish, dish_id)
        if not dish_item:
            return None
        dish_item.title = dish.title
        dish_item.description = dish.description
        dish_item.price = str(dish.price)
        await self.session.commit()
        await self.session.refresh(dish_item)
        return dish_item

    async def delete_dish(self, dish_id: uuid):
        dish_item = await self.session.get(Dish, dish_id)
        await self.session.delete(dish_item)
        await self.session.commit()
