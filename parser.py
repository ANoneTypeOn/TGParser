import configparser
import time
import json
from telethon.sync import TelegramClient
from telethon import connection
from datetime import date, datetime
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

url = input("Введите ссылку на канал или чат: ")
bot_token = input('Введите токен бота')

urlfile = url
arr = ['/']
for x in arr:
    urlfile = urlfile.replace(x, "|")

config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

client = TelegramClient(username, api_id, api_hash).start(bot_token=bot_token)

async def main():
    channel = await client.get_entity(url)
    await dump_all_participants(channel)


async def dump_all_participants(channel):
    offset_user = 0
    limit_user = 100
    all_participants = []
    all_part = []
    filter_user = ChannelParticipantsSearch('')

    while True:
        participants = await client(GetParticipantsRequest(channel, filter_user, offset_user, limit_user, hash=0))
        time.sleep(0.050)
        if not participants.users:
            break

        all_participants.extend(participants.users)
        offset_user += len(participants.users)
        all_part.extend(participants.users)
        offset_user += len(participants.users)

    ids = []
    all_users_details = []  # список словарей с интересующими параметрами участников канала

    for participant in all_part:
        ids.append(participant.id)

    for participant in all_participants:
        all_users_details.append({
            "id": participant.id,

            "first_name": participant.first_name,

            "last_name": participant.last_name,

            "user": participant.username,

            "phone": participant.phone,

            "is_bot": participant.bot})

    with open('{{users{0}}}.json'.format(urlfile), 'w', encoding='utf8') as outfile:
        json.dump(all_users_details, outfile, ensure_ascii=False, indent=4)

    with open('{{ids{0}}}.json'.format(urlfile), "w", encoding="utf8") as outfile:
        json.dump(ids, outfile, ensure_ascii=False)


with client:
    client.loop.run_until_complete(main())
