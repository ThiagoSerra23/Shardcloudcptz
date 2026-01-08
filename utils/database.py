import aiosqlite
import logging

DB_NAME = "bot_data.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS guild_config (
                guild_id INTEGER PRIMARY KEY,
                log_channel_id INTEGER,
                approval_channel_id INTEGER,
                voice_channel_id INTEGER,
                registration_channel_id INTEGER,
                cast_channel_id INTEGER,
                cast_message_id INTEGER,
                cast_role_id INTEGER,
                member_role_id INTEGER
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                user_id INTEGER PRIMARY KEY,
                referral TEXT,
                timestamp TEXT,
                status TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS registration_config (
                guild_id INTEGER PRIMARY KEY,
                panel_title TEXT DEFAULT 'Chupetaz',
                panel_description TEXT DEFAULT 'Bem-vindo ao Chupetaz!\nPara acessar nosso servidor, basta realizar o registro e aguardar a liberação da equipe.',
                panel_image TEXT,
                panel_footer TEXT DEFAULT 'discord.gg/chupetaz'
            )
        """)
        await db.commit()

async def get_config(guild_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM guild_config WHERE guild_id = ?", (guild_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {
                    "guild_id": row[0],
                    "log_channel_id": row[1],
                    "approval_channel_id": row[2],
                    "voice_channel_id": row[3],
                    "registration_channel_id": row[4],
                    "cast_channel_id": row[5],
                    "cast_message_id": row[6],
                    "cast_role_id": row[7],
                    "member_role_id": row[8]
                }
            return None

async def upsert_config(guild_id: int, **kwargs):
    current = await get_config(guild_id)
    if not current:
        current = {
            "guild_id": guild_id,
            "log_channel_id": None, 
            "approval_channel_id": None, 
            "voice_channel_id": None,
            "registration_channel_id": None,
            "cast_channel_id": None,
            "cast_message_id": None,
            "cast_role_id": None,
            "member_role_id": None
        }
    
    current.update(kwargs)
    
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT OR REPLACE INTO guild_config (
                guild_id, log_channel_id, approval_channel_id, voice_channel_id, 
                registration_channel_id, cast_channel_id, cast_message_id, cast_role_id, member_role_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            current["guild_id"],
            current["log_channel_id"],
            current["approval_channel_id"],
            current["voice_channel_id"],
            current["registration_channel_id"],
            current["cast_channel_id"],
            current["cast_message_id"],
            current["cast_role_id"],
            current["member_role_id"]
        ))
        await db.commit()

async def get_registration_config(guild_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM registration_config WHERE guild_id = ?", (guild_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {
                    "guild_id": row[0],
                    "panel_title": row[1],
                    "panel_description": row[2],
                    "panel_image": row[3],
                    "panel_footer": row[4]
                }
            return None

async def upsert_registration_config(guild_id: int, **kwargs):
    current = await get_registration_config(guild_id)
    if not current:
        current = {
            "guild_id": guild_id,
            "panel_title": "Chupetaz",
            "panel_description": "Bem-vindo ao Chupetaz!\nPara acessar nosso servidor, basta realizar o registro e aguardar a liberação da equipe.",
            "panel_image": None,
            "panel_footer": "discord.gg/chupetaz"
        }
    
    current.update(kwargs)
    
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT OR REPLACE INTO registration_config (
                guild_id, panel_title, panel_description, panel_image, panel_footer
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            current["guild_id"],
            current["panel_title"],
            current["panel_description"],
            current["panel_image"],
            current["panel_footer"]
        ))
        await db.commit()
