
from aiogram.types import *
from aiogram import Bot, types, executor, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import keyboards
import states
import WorkingWithDB as base
import parse
from aiogram.utils.markdown import *
import configparser
import teleparse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

config = configparser.ConfigParser()
config.read("config.ini")
BOT_TOKEN = config['Telegram']['bot_token']

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


logger = logging.getLogger(__name__)
logging.basicConfig(filename="debug.log", filemode="w", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', )

scheduler = AsyncIOScheduler()


def schedule():
    scheduler.add_job(main_func, 'interval', seconds=60, args=(dp,))


async def main_func(dp: Dispatcher):
    await teleparse.run_client()
    groups = await teleparse.get_all_groups()
    admins = base.DB.get_admins_list()
    a = []
    for group in groups:
        try:
            tmp = await teleparse.get_new_messages(group)
            if tmp is not None:
                a.append(tmp)
        except:
            pass
    for el in a:
        for mes in el:
            for admin in admins:
                try:
                    await bot.send_message(
                        admin,
                        text=text(f'В группе @'+str(mes['link']) + '\nИнтересное сообщение ' + 'от @' + str(mes['username']) + '\n' +
                                  mes['message'] + '\n' + ' от ' + str(mes['date'])),
                        reply_markup=keyboards.ReplyKeyboardRemove()
                    )
                except:
                    pass


# @dp.message_handler(commands=['run_client'], state='*')
# async def start_client(message: types.Message):
#     if message.from_user.id == 225529144:
        
#         await bot.send_message(
#             225529144,
#             text='Клиент запущен',
#             reply_markup=keyboards.ReplyKeyboardRemove()
#         )


@dp.message_handler(commands=['add_new_user'], state='*')
async def start_client(message: types.Message):
    base.DB.add_new_admin(message.from_user.id)
    await bot.send_message(
        message.from_user.id,
        text='Вы успешно подписались на рассылку',
        reply_markup=keyboards.ReplyKeyboardRemove()
    )


@dp.message_handler(commands=['help'], state='*')
async def help(message: types.Message):
    await states.FSMUser.choose_action.set()
    await bot.send_message(
        message.from_user.id,
        text='Выберите действие',
        reply_markup=keyboards.actions_with_chats_kb
    )
    await states.FSMUser.choose_actions_with_chats.set()


@dp.message_handler(lambda c: c.text == 'Список каналов', state=states.FSMUser.choose_actions_with_chats)
async def keywords_list(message: types.Message):
    a = base.DB.get_all_chats()
    await bot.send_message(
        message.from_user.id,
        text=text(a),
        reply_markup=keyboards.ReplyKeyboardRemove()
    )


@dp.message_handler(lambda c: c.text == 'Список ключевых слов', state=states.FSMUser.choose_actions_with_chats)
async def channel_list(message: types.Message):
    a = base.DB.get_all_keywords()
    await bot.send_message(
        message.from_user.id,
        text=text(a),
        reply_markup=keyboards.ReplyKeyboardRemove()
    )


@dp.message_handler(lambda c: c.text == 'Добавить канал', state=states.FSMUser.choose_actions_with_chats)
async def adding_new_channel(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        text=text('Отправьте ссылку (https://t.me/dubai_pro_life)'),
        reply_markup=keyboards.ReplyKeyboardRemove()
    )
    await states.FSMUser.adding_new_channel.set()


@dp.message_handler(state=states.FSMUser.adding_new_channel)
async def typing_link(message: types.Message):
    try:
        await teleparse.join_group(message.text)
        base.DB.add_chat(message.text)
        await bot.send_message(
            message.from_user.id,
            text=text('Добавлен'),
            reply_markup=keyboards.ReplyKeyboardRemove()
        )
    except:
        await bot.send_message(
            message.from_user.id,
            text=text('Неверная ссылка'),
            reply_markup=keyboards.ReplyKeyboardRemove()
        )


@dp.message_handler(lambda c: c.text == 'Добавить ключевое слово', state=states.FSMUser.choose_actions_with_chats)
async def choose_add_action(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        text=text('Введите ключевые слова("RUB, AED")'),
        reply_markup=keyboards.ReplyKeyboardRemove()
    )
    await states.FSMUser.typing_keyword.set()


@dp.message_handler(lambda c: c.text == 'Удалить ключевое слово', state=states.FSMUser.choose_actions_with_chats)
async def schoose_delete_action(message: types.Message):
    lst = base.DB.get_all_keywords()
    await bot.send_message(
        message.from_user.id,
        text=text('Укажите индексы слов, которые хотите удалить("1,2,3")'),
        reply_markup=keyboards.ReplyKeyboardRemove()
    )
    await bot.send_message(
        message.from_user.id,
        text=text(lst),
        reply_markup=keyboards.ReplyKeyboardRemove()
    )

    await states.FSMUser.delete_keyword.set()


@dp.message_handler(state=states.FSMUser.delete_keyword)
async def delete_keyword(message: types.Message):
    base.DB.delete_keyword_by_id(message.text)
    await bot.send_message(
        message.from_user.id,
        text=text('Удалено'),
        reply_markup=keyboards.ReplyKeyboardRemove()
    )
    await states.FSMUser.typing_keyword.set()


@dp.message_handler(state=states.FSMUser.typing_keyword)
async def follow_list(message: types.Message):
    base.DB.add_new_keyword(message.text)
    await bot.send_message(
        message.from_user.id,
        text=text(message.text + ' добавлено'),
        reply_markup=keyboards.ReplyKeyboardRemove()
    )
    await states.FSMUser.typing_keyword.set()


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message):
    await states.FSMUser.choose_action.set()
    await bot.send_message(
        message.from_user.id,
        text='Выберите действие',
        reply_markup=keyboards.help_kb
    )
    await states.FSMUser.choose_action.set()


@dp.message_handler(lambda c: c.text == 'Список отслеживаемых каналов', state=states.FSMUser.choose_action)
async def follow_list(message: types.Message):
    lst = base.DB.get_all_chats()
    await bot.send_message(
        message.from_user.id,
        text=text('Каналы\n' + lst),
        reply_markup=keyboards.ReplyKeyboardRemove()
    )


@dp.message_handler(lambda c: c.text == 'Список ключевых слов', state=states.FSMUser.choose_action)
async def follow_list(message: types.Message):
    lst = base.DB.get_all_keywords()
    await bot.send_message(
        message.from_user.id,
        text=text('Слова\n' + lst),
        reply_markup=keyboards.ReplyKeyboardRemove()
    )

    # await states.FSMUser.type_keyword.set()


@dp.message_handler(lambda c: c.text == 'Поиск по ключевому слову', state=states.FSMUser.choose_action)
async def search_posts(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        text=text('Введите ключевое слово'),
        reply_markup=keyboards.ReplyKeyboardRemove()
    )

    await states.FSMUser.type_keyword.set()


@dp.message_handler(state=states.FSMUser.type_keyword)
async def find_info(message: types.Message):
    keyword = message.text
    lst = []
    try:
        await bot.send_message(
            message.from_user.id,
            text=text('Операция выполняется, ожидайте'),
            reply_markup=keyboards.ReplyKeyboardRemove(),
            parse_mode=ParseMode.MARKDOWN
        )
        lst = parse.getinfo(keyword=keyword)
        if len(lst) == 0:
            await bot.send_message(
                message.from_user.id,
                text=text('Ничего не найдено'),
                # text= text('<a href='{{i['link']}}'>Пост</a> <br><p>{{i['content']}}</p>'),
                reply_markup=keyboards.ReplyKeyboardRemove(),
            )

    except:
        pass
    finally:
        for i in lst:
            await bot.send_message(
                message.from_user.id,
                text=text(link('Пост', i['link']), '\n', i['content']),
                # text= text('<a href='{{i['link']}}'>Пост</a> <br><p>{{i['content']}}</p>'),
                reply_markup=keyboards.ReplyKeyboardRemove(),
                parse_mode=ParseMode.MARKDOWN
            )


@dp.message_handler(lambda c: c.text == 'Изменить список каналов', state=states.FSMUser.choose_action)
async def change_channesl_list(message: types.Message):
    lst = base.DB.get_channel_lists()
    await bot.send_message(
        message.from_user.id,
        text=text('Текущие каналы\n', lst),
        reply_markup=keyboards.ReplyKeyboardRemove()
    )
    await bot.send_message(
        message.from_user.id,
        text=text('Что будем делать?'),
        reply_markup=keyboards.actions_with_channels_kb
    )

    await states.FSMUser.add_or_remove_action.set()


@dp.message_handler(lambda c: c.text == 'Добавить', state=states.FSMUser.add_or_remove_action)
async def add_channel(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        text=text('Введите адреса каналов через запятую\n', 'Пример:',
                  code('Ateobreaking, prg_memes, lentachold')),
        reply_markup=keyboards.ReplyKeyboardRemove(),
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await states.FSMUser.add_new_channel.set()


@dp.message_handler(state=states.FSMUser.add_new_channel)
async def add_new_channel(message: types.Message):
    content = message.text
    base.DB.add_channels(content=content)
    await bot.send_message(
        message.from_user.id,
        text=text('Каналы успешно добавлены\nВозвращаюсь в меню'),
        reply_markup=keyboards.ReplyKeyboardRemove(),
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await states.FSMUser.beginning.set()


@dp.message_handler(lambda c: c.text == 'Удалить', state=states.FSMUser.add_or_remove_action)
async def delete_channel(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        text=text('Введите id каналов, которые хотите удалить', 'Пример:',
                  code('1,2,3')),
        reply_markup=keyboards.ReplyKeyboardRemove(),
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await states.FSMUser.delete_channels.set()


@dp.message_handler(state=states.FSMUser.delete_channels)
async def add_new_channel(message: types.Message):
    content = message.text
    try:
        base.DB.delete_channels(content=content)
    except:
        await bot.send_message(
            message.from_user.id,
            text=text('Неверный ввод. Попробуйте еще раз /start'),
            reply_markup=keyboards.ReplyKeyboardRemove(),
        )
        return
    lst = base.DB.get_channel_lists()
    await bot.send_message(
        message.from_user.id,
        text=text('Каналы успешно удалены'),
        reply_markup=keyboards.ReplyKeyboardRemove(),
    )
    await bot.send_message(
        message.from_user.id,
        text=text(f'Текущие каналы:\n{lst}\n', 'Возвращаюсь в меню'),
        reply_markup=keyboards.ReplyKeyboardRemove(),
    )
    await states.FSMUser.beginning.set()

if __name__ == '__main__':
    print('started')
    scheduler.start()
    schedule()
    executor.start_polling(dp, skip_updates=False)
