# ────────────────────────────────────────────────────────────────
# ✅ THIS PROJECT IS DEVELOPED AND MAINTAINED BY @trinityXmods (TELEGRAM)
# 🚫 DO NOT REMOVE OR ALTER THIS CREDIT LINE UNDER ANY CIRCUMSTANCES.
# ⭐ FOR MORE HIGH-QUALITY OPEN-SOURCE BOTS, FOLLOW US ON GITHUB.
# 🔗 OFFICIAL GITHUB: https://github.com/Trinity-Mods
# 📩 NEED HELP OR HAVE QUESTIONS? REACH OUT VIA TELEGRAM: @velvetexams
# ────────────────────────────────────────────────────────────────

import motor.motor_asyncio
from config import ADMINS, DB_URL, DB_NAME

dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
database = dbclient[DB_NAME]

user_data    = database['users']
admin_data   = database['admins']
link_data    = database['links']
batch_data   = database['batches']
channel_data = database['db_channels']

default_verify = {
    'is_verified': False,
    'verified_time': 0,
    'verify_token': "",
    'link': ""
}

def new_user(id):
    return {
        '_id': id,
        'verify_status': {
            'is_verified': False,
            'verified_time': "",
            'verify_token': "",
            'link': ""
        }
    }

# ── db channels ────────────────────────────────────────────────
async def add_db_channel(channel_id: int):
    await channel_data.update_one({'_id': channel_id}, {'$set': {'_id': channel_id}}, upsert=True)

async def remove_db_channel(channel_id: int):
    await channel_data.delete_one({'_id': channel_id})

async def get_db_channels():
    docs = channel_data.find()
    return [doc['_id'] async for doc in docs]

# ── links ──────────────────────────────────────────────────────
async def new_link(hash: str):
    return {'clicks': 0, 'hash': hash}

async def gen_new_count(hash: str):
    data = await new_link(hash)
    await link_data.insert_one(data)

async def present_hash(hash: str):
    found = await link_data.find_one({"hash": hash})
    return bool(found)

async def inc_count(hash: str):
    data = await link_data.find_one({'hash': hash})
    clicks = data.get('clicks')
    await link_data.update_one({'hash': hash}, {'$set': {'clicks': clicks + 1}})

async def get_clicks(hash: str):
    data = await link_data.find_one({'hash': hash})
    return data.get('clicks')

# ── batches ────────────────────────────────────────────────────
async def store_batch(key: str, msg_ids: list):
    await batch_data.update_one(
        {'_id': key},
        {'$set': {'msg_ids': msg_ids}},
        upsert=True
    )

async def get_batch(key: str):
    doc = await batch_data.find_one({'_id': key})
    return doc['msg_ids'] if doc else None

# ── users ──────────────────────────────────────────────────────
async def present_user(user_id: int):
    found = await user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user = new_user(user_id)
    await user_data.insert_one(user)

async def db_verify_status(user_id):
    user = await user_data.find_one({'_id': user_id})
    if user:
        return user.get('verify_status', default_verify)
    return default_verify

async def db_update_verify_status(user_id, verify):
    await user_data.update_one({'_id': user_id}, {'$set': {'verify_status': verify}})

async def full_userbase():
    user_docs = user_data.find()
    user_ids = [doc['_id'] async for doc in user_docs]
    return user_ids

async def del_user(user_id: int):
    await user_data.delete_one({'_id': user_id})

# ── admins ─────────────────────────────────────────────────────
async def present_admin(user_id: int):
    found = await admin_data.find_one({'_id': user_id})
    return bool(found)

async def add_admin(user_id: int):
    user = new_user(user_id)
    await admin_data.insert_one(user)
    ADMINS.append(int(user_id))

async def del_admin(user_id: int):
    await admin_data.delete_one({'_id': user_id})
    ADMINS.remove(int(user_id))

async def full_adminbase():
    user_docs = admin_data.find()
    user_ids = [int(doc['_id']) async for doc in user_docs]
    return user_ids

# ────────────────────────────────────────────────────────────────
# ✅ THIS PROJECT IS DEVELOPED AND MAINTAINED BY @trinityXmods (TELEGRAM)
# 🚫 DO NOT REMOVE OR ALTER THIS CREDIT LINE UNDER ANY CIRCUMSTANCES.
# ⭐ FOR MORE HIGH-QUALITY OPEN-SOURCE BOTS, FOLLOW US ON GITHUB.
# 🔗 OFFICIAL GITHUB: https://github.com/Trinity-Mods
# 📩 NEED HELP OR HAVE QUESTIONS? REACH OUT VIA TELEGRAM: @velvetexams
# ────────────────────────────────
