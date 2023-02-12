from re import S
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


class FSMUser(StatesGroup):
    beginning = State()
    choose_action = State()
    add_or_remove_action = State()
    change_channels_list = State()
    add_new_channel = State()
    delete_channels = State()
    type_keyword = State()
    add_new_link = State()
    choose_actions_with_chats = State()
    typing_keyword = State()
    delete_keyword = State()
    adding_new_channel = State()
