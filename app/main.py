import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.utils.formatting import Text
from aiogram.utils.markdown import hbold, hlink
from aiogram.types import Message
from requests_html import HTMLSession


from misc import logger
from config import settings
from scraper import OLXParser
from bot.keyboards import make_row_keyboard
from bot.proxy import router as proxy_router

dp = Dispatcher()
dp.include_router(proxy_router)

start_buttons = ['💾 Прокси', '🎇 Начать работу']


def get_links(session, proxy_data):
    proxy = {
        'https': f'http://{proxy_data}'
    }
    
    parser = OLXParser(session, proxy)

    return parser.get_all()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        text='OLX бот приветсвует Вас!\nВведите прокси и начинайте парсинг!',
        reply_markup=make_row_keyboard(start_buttons)
    )


@dp.message(F.text == '🎇 Начать работу')
async def command_start_work(
    message: Message,
    state: FSMContext
) -> None:
    try:
        proxy_data = await state.get_data()
    except Exception as e:
        logger.warning(e)
        await message.answer('Сначала Вам нужно ввести прокси!')
    else:
        if 'proxy_data' in proxy_data.keys():
            session = HTMLSession()

            await message.answer('Идет парсинг...')

            while True:
                links = get_links(
                    session, 
                    proxy_data['proxy_data']
                )

                if len(links) > 0:
                    for link in links:
                        msg = Text()
                        msg = f'{hlink(link["title"], link["link"])} 🆕\n{hlink("", link["img"])}'
                        await message.answer(msg)
                        await asyncio.sleep(1)

                    logger.info(f'Parsing result: {len(links)} links')

                await asyncio.sleep(60)
        else:
            await message.answer('Сначала Вам нужно ввести прокси!')


async def main() -> None:
    bot = Bot(
        settings.BOT_TOKEN.get_secret_value(),
        parse_mode=ParseMode.HTML
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
