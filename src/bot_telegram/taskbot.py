from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import service
from bot_telegram.keybords import get_task_keyboard, main_keyboard
from config import settings
from schemas import CreateTask

storage = MemoryStorage()
bot = Bot(settings.API_TOKEN)
dp = Dispatcher(bot, storage=storage)


class BotStateGroup(StatesGroup):
    task = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    """Welcomes the user and adding it to the database if it doesn't exist"""
    db = message.bot.get('db')
    async with db() as session:
        await service.create_user_if_not_exist(
            user_id=message.from_user.id,
            username=message.from_user.username,
            session=session)
    await message.answer(
        "*Привет!* \nДля добавления задачи выполните команду `/add` \n"
        'Чтобы посмотреть задачи выполните команду `/list`',
        parse_mode='Markdown',
        reply_markup=main_keyboard)
    await message.delete()


@dp.message_handler(commands=['add'])
async def cmd_add_task(message: types.Message) -> None:
    """Checks the number of user tasks
    and changes the state of the bot to add a new task
    """
    db = message.bot.get('db')
    async with db() as session:
        limit = await service.has_task_limit(
            message.from_user.id, session=session)
    if not limit:
        return await message.answer('Превышен лимит задач')
    await message.answer('Введите задачу', reply_markup=main_keyboard)
    await BotStateGroup.task.set()
    await message.delete()


@dp.message_handler(state=BotStateGroup.task)
async def task_entry(message: types.Message, state: FSMContext) -> None:
    """Adds a new user task"""
    db = message.bot.get('db')
    async with db() as session:
        new_task = CreateTask(
            user_id=message.from_user.id, title=message.text)
        service.add_task_to_session(task=new_task, session=session)
        await session.commit()
        await state.finish()
        await message.reply('Задача добавлена')


@dp.message_handler(commands=['list'])
async def cmd_list_task(message: types.Message) -> None:
    """Display all user tasks"""
    db = message.bot.get('db')
    async with db() as session:
        tasks = await service.get_user_tasks(
            user_id=message.from_user.id,
            session=session)
        if tasks:
            task_keyboard = get_task_keyboard(tasks=tasks)
            await message.answer(
                'Списко ваших задач', reply_markup=task_keyboard)
        else:
            await message.answer(
                'У вас нет задач.\n'
                'Что бы добавить задчу введите команду `/add`',
                parse_mode='Markdown',
                reply_markup=main_keyboard)
        await message.delete()


@dp.callback_query_handler()
async def remove_task_callback(callback: types.CallbackQuery):
    """Deletes the task and displays the updated inlinekeyboard"""
    db = callback.message.bot.get('db')
    task_id = int(callback.data)
    async with db() as session:
        await service.delete_task(task_id=task_id, session=session)
        user = await service.get_user_by_id(
            user_id=callback.from_user.id,
            session=session)
        if user and user.tasks:
            task_keyboard = get_task_keyboard(tasks=user.tasks)
            await callback.message.edit_reply_markup(task_keyboard)
        else:
            await callback.message.delete()
