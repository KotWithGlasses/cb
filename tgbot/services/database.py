import json

from asyncpg import Connection, create_pool

class Database:
    def __init__(self, config):
        self.config = config
        self.pool: Connection = None

    async def connect(self):
        self.pool = await create_pool(
            host=self.config.db.host,
            user=self.config.db.user,
            password=self.config.db.password,
            database=self.config.db.database
        )

    async def disconnect(self):
        if self.pool:
            await self.pool.close()

    async def execute(self, query, *args):
        # INSERT, UPDATE, DELETE
        async with self.pool.acquire() as connection:
            result = await connection.execute(query, *args)
            return result

    async def fetch(self, query, *args):
        # SELECT
        async with self.pool.acquire() as connection:
            result = await connection.fetch(query, *args)

             # Преобразование объекта Record в список словарей
            result_data = [dict(record.items()) for record in result]
            return json.dumps(result_data)
