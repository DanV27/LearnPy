---
title: AsyncIO
summary: Concurrency with async/await — run many slow I/O operations at the same time without threads.
related: generators, decorators, context-managers
---

`asyncio` is Python's built-in way to run thousands of I/O-bound tasks concurrently on a single thread. It's not for speeding up CPU work — for that you'd use processes — but it's perfect for making lots of HTTP requests, database queries, or socket connections happen at the same time.

The mental model: **`await` is "let other tasks run while we wait"**. When an `async` function hits `await some_slow_thing()`, it parks, the event loop hands control to another waiting task, and the original function resumes when its slow thing finishes.

## Hello, asyncio

```python
import asyncio

async def say_after(delay: float, message: str) -> None:
    await asyncio.sleep(delay)
    print(message)

async def main() -> None:
    await say_after(1, "hello")
    await say_after(1, "world")

asyncio.run(main())     # prints "hello", then "world" — takes 2 seconds
```

That ran sequentially. To run things **concurrently**, use `asyncio.gather`:

```python
async def main() -> None:
    await asyncio.gather(
        say_after(1, "hello"),
        say_after(1, "world"),
    )

asyncio.run(main())     # prints both — takes 1 second
```

Both `say_after` calls slept at the same time. That's the whole point.

## A real example: fetch many URLs at once

```python
import asyncio
import aiohttp

async def fetch(session, url: str) -> int:
    async with session.get(url) as resp:
        return resp.status

async def main(urls: list[str]) -> list[int]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, u) for u in urls]
        return await asyncio.gather(*tasks)

statuses = asyncio.run(main([
    "https://python.org",
    "https://example.com",
    "https://httpbin.org/get",
]))
print(statuses)
```

Three HTTP requests run at the same time on one thread.

## Rules of thumb

- An `async def` function returns a **coroutine** — calling it doesn't run it. You need `await`, `asyncio.run`, or `asyncio.create_task` to actually execute it.
- You can only `await` inside an `async def`.
- Don't call `time.sleep` inside async code — it blocks the whole event loop. Use `await asyncio.sleep(...)`.
- Don't reach for asyncio if your bottleneck is CPU — use `concurrent.futures.ProcessPoolExecutor` instead.

If [Generators](/lesson/generators) made sense, asyncio's mechanics will too — they share the "pause and resume" idea.
