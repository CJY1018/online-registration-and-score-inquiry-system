import asyncio
import aioredis
import time


async def main():
    # Redis client bound to single connection (no auto reconnection).
    redis = aioredis.from_url(
        "redis://localhost", encoding="utf-8", decode_responses=True
    )

    async with redis.client() as conn:
        await conn.set("my-key1", "value")
        val = await conn.get("my-key1")
    print(val)


async def redis_pool():
    # Redis client bound to pool of connections (auto-reconnecting).
    redis = aioredis.from_url(
        "redis://localhost", encoding="utf-8", decode_responses=True
    )
    await redis.set("my-key2", "value")
    val = await redis.get("my-key2")
    print(val)


if __name__ == "__main__":
    # 初始时间
    start = time.time()
    asyncio.run(redis_pool())
    # 结束时间
    end = time.time()
    print('连接池耗时：', end - start)

    # 初始时间
    start = time.time()
    asyncio.run(main())
    # 结束时间
    end = time.time()
    print('单连接耗时：', end - start)

    # 初始时间
    start = time.time()
    asyncio.run(redis_pool())
    # 结束时间
    end = time.time()
    print('连接池耗时：', end - start)

    # 初始时间
    start = time.time()
    asyncio.run(main())
    # 结束时间
    end = time.time()
    print('单连接耗时：', end - start)
