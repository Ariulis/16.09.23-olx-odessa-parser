from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

router = Router()


class GetProxy(StatesGroup):
    proxy_data = State()


@router.message(F.text == '💾 Прокси')
async def add_proxy(
    message: Message,
    state: FSMContext
) -> None:
    await message.answer('Введите Ваш прокси\nПример:\n"proxy_login:proxy_password@proxy_ip:proxy_port"')

    await state.set_state(GetProxy.proxy_data)


@router.message(GetProxy.proxy_data)
async def give_proxy(
    message: Message,
    state: FSMContext
) -> None:
    await state.update_data(proxy_data=message.text)
    proxy_data = await state.get_data()
    print(proxy_data)
    await message.answer('Прокси сохранен. Можно приступать к парсингу!')
