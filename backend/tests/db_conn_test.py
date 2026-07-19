import asyncio
from psycopg_pool import AsyncConnectionPool


async def main():
    async with AsyncConnectionPool("postgresql://postgres:postgres@192.168.1.17:5433/app_db",
    min_size=2, max_size=10, open=False) as pool:
        async with pool.connection() as conn:            
            print(conn)

if __name__ == "__main__":
    asyncio.run(main())


