import asyncio
import aiohttp
import aiofiles
import sys
import os
import logging


logging.basicConfig(filename="artifacts/log.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
log_info = logging.getLogger("log_info")


async def download_images(session, i):
    log_info.debug(f"Start download image {i}")
    url = "https://picsum.photos/1000/1000"
    try:
        async with session.get(url) as img:
            async with aiofiles.open(os.path.join("artifacts", f"image_{i}.jpg"), "wb") as output:
                await output.write(await img.read())
                log_info.debug(f"Uploaded image {i}")
    except Exception as e:
        log_info.error(e)


async def get_images(n):
    async with aiohttp.ClientSession() as session:
        log_info.debug("start to send tasks in queue")
        tasks = [asyncio.create_task(download_images(session, i)) for i in range(n)]
        try:
            log_info.debug("finish to send tasks in queue, wait results")
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            log_info.error(e)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    asyncio.run(get_images(n))