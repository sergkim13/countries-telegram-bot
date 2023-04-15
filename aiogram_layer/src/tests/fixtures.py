from datetime import datetime

import pytest
import pytest_asyncio
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Chat, Message, Update, User

from aiogram_layer.src.app import dp
from aiogram_layer.src.tests.mocks import MockedBot


@pytest.fixture()
def bot():
    bot = MockedBot()
    token = Bot.set_current(bot)
    try:
        yield bot
    finally:
        Bot.reset_current(token)


@pytest_asyncio.fixture(scope='function')
async def dispatcher(state: FSMContext, bot: Bot, state_data: dict):
    current_state = dp.fsm.get_context(bot=bot, user_id=TEST_USER.id, chat_id=TEST_USER_CHAT.id)
    await current_state.set_state(state)
    await current_state.update_data(data=state_data)
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()


@pytest_asyncio.fixture(scope='session')
async def storage():
    mem_storage = MemoryStorage()
    try:
        yield mem_storage
    finally:
        await mem_storage.close()


TEST_USER = User(id=123, is_bot=False, first_name='User', last_name='Bot', username='test',
                 language_code='ru-RU', is_premium=False, added_to_attachment_menu=None, can_join_groups=None,
                 can_read_all_group_messages=None, supports_inline_queries=None)

TEST_USER_CHAT = Chat(id=12, type='private', title=None, username=TEST_USER.username, first_name=TEST_USER.first_name,
                      last_name=TEST_USER.last_name, is_forum=None, photo=None,
                      active_usernames=None, emoji_status_custom_emoji_id=None, bio=None, has_private_forwards=None,
                      has_restricted_voice_and_video_messages=None, join_to_send_messages=None, join_by_request=None,
                      description=None, invite_link=None, pinned_message=None, permissions=None, slow_mode_delay=None,
                      message_auto_delete_time=None, has_aggressive_anti_spam_enabled=None, has_hidden_members=None,
                      has_protected_content=None, sticker_set_name=None, can_set_sticker_set=None, linked_chat_id=None,
                      location=None)


def get_message(text: str):
    return Message(message_id=123, date=datetime.now(), chat=TEST_USER_CHAT, message_thread_id=None,
                   from_user=TEST_USER, sender_chat=TEST_USER_CHAT,
                   forward_from=None, forward_from_chat=None, forward_from_message_id=None, forward_signature=None,
                   forward_sender_name=None, forward_date=None, is_topic_message=None, is_automatic_forward=None,
                   reply_to_message=None, via_bot=None, edit_date=None, has_protected_content=None, media_group_id=None,
                   author_signature=None, text=text, entities=None, animation=None, audio=None, document=None,
                   photo=None, sticker=None, video=None, video_note=None, voice=None, caption=None,
                   caption_entities=None, has_media_spoiler=None, contact=None, dice=None, game=None, poll=None,
                   venue=None, location=None, new_chat_members=None, left_chat_member=None, new_chat_title=None,
                   new_chat_photo=None, delete_chat_photo=None, group_chat_created=None, supergroup_chat_created=None,
                   channel_chat_created=None, message_auto_delete_timer_changed=None, migrate_to_chat_id=None,
                   migrate_from_chat_id=None, pinned_message=None, invoice=None, successful_payment=None,
                   user_shared=None, chat_shared=None, connected_website=None, write_access_allowed=None,
                   passport_data=None, proximity_alert_triggered=None, forum_topic_created=None,
                   forum_topic_edited=None, forum_topic_closed=None, forum_topic_reopened=None,
                   general_forum_topic_hidden=None, general_forum_topic_unhidden=None, video_chat_scheduled=None,
                   video_chat_started=None, video_chat_ended=None, video_chat_participants_invited=None,
                   web_app_data=None, reply_markup=None)


def get_callback_query(query: str):
    return CallbackQuery(id='885', from_user=TEST_USER, chat_instance=str(TEST_USER_CHAT.id),
                         message=get_message('/start'), inline_message_id=None, data=query, game_short_name=None)


def get_update(message: Message = None, call: CallbackQuery = None):
    return Update(update_id=187, message=message, edited_message=None, channel_post=None, edited_channel_post=None,
                  inline_query=None, chosen_inline_result=None, callback_query=call, shipping_query=None,
                  pre_checkout_query=None, poll=None, poll_answer=None, my_chat_member=None, chat_member=None,
                  chat_join_request=None)
