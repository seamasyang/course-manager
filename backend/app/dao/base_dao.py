import logging

from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row

from app.models import settings


logger = logging.getLogger(__name__)


pool = None
async def create_pool():
    global pool
    try:
        pool = AsyncConnectionPool(
            settings.database_url,
            min_size=2,
            max_size=5,
            open=False,
            kwargs={'row_factory': dict_row}
        )
    except Exception as e:
        logger.error(f"Failed to create connection pool: {e}")
        pool = None
        raise
    finally:
        if pool is None:
            logger.warning("Connection pool was not created successfully")


async def close_pool():
    global pool
    if pool:
        try:
            await pool.close()
        except Exception as e:
            logger.error(f"Failed to close connection pool: {e}")
        finally:
            pool = None


class BaseDAO:
    _pool = None

    async def _get_pool(self):
        if self._pool is None:
            try:
                self._pool = pool
                await self._pool.open()
            except Exception as e:
                logger.error(f"Failed to open connection pool: {e}")
                self._pool = None
                raise

        return self._pool

    async def fetch_all(self, sql: str, params=()) -> list[dict]:
        pool = await self._get_pool()
        async with pool.connection() as conn:
            try:
                cur = await conn.execute(sql, params)
                rows = await cur.fetchall() or []
                return rows
            except Exception as e:
                logger.error(f"fetch_all failed: {e}, SQL: {sql}, params: {params}")
                raise

    async def fetch_one(self, sql: str, params=()) -> dict | None:
        pool = await self._get_pool()
        async with pool.connection() as conn:
            try:
                cur = await conn.execute(sql, params)
                row = await cur.fetchone()
                return row
            except Exception as e:
                logger.error(f"fetch_one failed: {e}, SQL: {sql}, params: {params}")
                raise

    async def execute(self, sql: str, params=()) -> int:
        pool = await self._get_pool()
        async with pool.connection() as conn:
            try:
                async with conn.cursor() as cur:
                    await cur.execute(sql, params)
                    await conn.commit()
                    return cur.rowcount
            except Exception as e:
                logger.error(f"execute failed: {e}, SQL: {sql}, params: {params}")
                await conn.rollback()
                raise